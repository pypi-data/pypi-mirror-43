/*
Copyright (c) 2007-2016 Contributors as noted in the AUTHORS file

This file is part of libzmq, the ZeroMQ core engine in C++.

libzmq is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License (LGPL) as published
by the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

As a special exception, the Contributors give you permission to link
this library with independent modules to produce an executable,
regardless of the license terms of these independent modules, and to
copy and distribute the resulting executable under terms of your choice,
provided that you also meet, for each linked independent module, the
terms and conditions of the license of that module. An independent
module is a module which is not derived from or based on this library.
If you modify this library, you must extend this exception to your
version of the library.

libzmq is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "precompiled.hpp"

#if !defined ZMQ_HAVE_WINDOWS
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#ifdef ZMQ_HAVE_VXWORKS
#include <sockLib.h>
#endif
#endif

#include "udp_address.hpp"
#include "udp_engine.hpp"
#include "session_base.hpp"
#include "err.hpp"
#include "ip.hpp"

//  OSX uses a different name for this socket option
#ifndef IPV6_ADD_MEMBERSHIP
#define IPV6_ADD_MEMBERSHIP IPV6_JOIN_GROUP
#endif

#ifdef __APPLE__
#include <TargetConditionals.h>
#endif

zmq::udp_engine_t::udp_engine_t (const options_t &options_) :
    _plugged (false),
    _fd (-1),
    _session (NULL),
    _handle (static_cast<handle_t> (NULL)),
    _address (NULL),
    _options (options_),
    _send_enabled (false),
    _recv_enabled (false)
{
}

zmq::udp_engine_t::~udp_engine_t ()
{
    zmq_assert (!_plugged);

    if (_fd != retired_fd) {
#ifdef ZMQ_HAVE_WINDOWS
        int rc = closesocket (_fd);
        wsa_assert (rc != SOCKET_ERROR);
#else
        int rc = close (_fd);
        errno_assert (rc == 0);
#endif
        _fd = retired_fd;
    }
}

int zmq::udp_engine_t::init (address_t *address_, bool send_, bool recv_)
{
    zmq_assert (address_);
    zmq_assert (send_ || recv_);
    _send_enabled = send_;
    _recv_enabled = recv_;
    _address = address_;

    _fd = open_socket (_address->resolved.udp_addr->family (), SOCK_DGRAM,
                       IPPROTO_UDP);
    if (_fd == retired_fd)
        return -1;

    unblock_socket (_fd);

    return 0;
}

void zmq::udp_engine_t::plug (io_thread_t *io_thread_, session_base_t *session_)
{
    zmq_assert (!_plugged);
    _plugged = true;

    zmq_assert (!_session);
    zmq_assert (session_);
    _session = session_;

    //  Connect to I/O threads poller object.
    io_object_t::plug (io_thread_);
    _handle = add_fd (_fd);

    const udp_address_t *const udp_addr = _address->resolved.udp_addr;

    // Bind the socket to a device if applicable
    if (!_options.bound_device.empty ())
        bind_to_device (_fd, _options.bound_device);

    if (_send_enabled) {
        if (!_options.raw_socket) {
            const ip_addr_t *out = udp_addr->target_addr ();
            _out_address = out->as_sockaddr ();
            _out_address_len = out->sockaddr_len ();

            if (out->is_multicast ()) {
                int level;
                int optname;

                if (out->family () == AF_INET6) {
                    level = IPPROTO_IPV6;
                    optname = IPV6_MULTICAST_LOOP;
                } else {
                    level = IPPROTO_IP;
                    optname = IP_MULTICAST_LOOP;
                }

                int loop = _options.multicast_loop;
                int rc =
                  setsockopt (_fd, level, optname,
                              reinterpret_cast<char *> (&loop), sizeof (loop));

#ifdef ZMQ_HAVE_WINDOWS
                wsa_assert (rc != SOCKET_ERROR);
#else
                errno_assert (rc == 0);
#endif

                int hops = _options.multicast_hops;

                if (hops > 0) {
                    rc = setsockopt (_fd, level, IP_MULTICAST_TTL,
                                     reinterpret_cast<char *> (&hops),
                                     sizeof (hops));
                } else {
                    rc = 0;
                }

#ifdef ZMQ_HAVE_WINDOWS
                wsa_assert (rc != SOCKET_ERROR);
#else
                errno_assert (rc == 0);
#endif
                if (out->family () == AF_INET6) {
                    int bind_if = udp_addr->bind_if ();

                    if (bind_if > 0) {
                        //  If a bind interface is provided we tell the
                        //  kernel to use it to send multicast packets
                        rc = setsockopt (_fd, IPPROTO_IPV6, IPV6_MULTICAST_IF,
                                         reinterpret_cast<char *> (&bind_if),
                                         sizeof (bind_if));
                    } else {
                        rc = 0;
                    }
                } else {
                    struct in_addr bind_addr =
                      udp_addr->bind_addr ()->ipv4.sin_addr;

                    if (bind_addr.s_addr != INADDR_ANY) {
                        rc = setsockopt (_fd, IPPROTO_IP, IP_MULTICAST_IF,
                                         reinterpret_cast<char *> (&bind_addr),
                                         sizeof (bind_addr));
                    } else {
                        rc = 0;
                    }
                }

#ifdef ZMQ_HAVE_WINDOWS
                wsa_assert (rc != SOCKET_ERROR);
#else
                errno_assert (rc == 0);
#endif
            }
        } else {
            /// XXX fixme ?
            _out_address = reinterpret_cast<sockaddr *> (&_raw_address);
            _out_address_len = sizeof (sockaddr_in);
        }

        set_pollout (_handle);
    }

    if (_recv_enabled) {
        int on = 1;
        int rc = setsockopt (_fd, SOL_SOCKET, SO_REUSEADDR,
                             reinterpret_cast<char *> (&on), sizeof (on));
#ifdef ZMQ_HAVE_WINDOWS
        wsa_assert (rc != SOCKET_ERROR);
#else
        errno_assert (rc == 0);
#endif

        const ip_addr_t *bind_addr = udp_addr->bind_addr ();
        ip_addr_t any = ip_addr_t::any (bind_addr->family ());
        const ip_addr_t *real_bind_addr;

        bool multicast = udp_addr->is_mcast ();

        if (multicast) {
        //  Multicast addresses should be allowed to bind to more than
        //  one port as all ports should receive the message
#ifdef SO_REUSEPORT
            rc = setsockopt (_fd, SOL_SOCKET, SO_REUSEPORT,
                             reinterpret_cast<char *> (&on), sizeof (on));
#ifdef ZMQ_HAVE_WINDOWS
            wsa_assert (rc != SOCKET_ERROR);
#else
            errno_assert (rc == 0);
#endif
#endif

            //  In multicast we should bind ANY and use the mreq struct to
            //  specify the interface
            any.set_port (bind_addr->port ());

            real_bind_addr = &any;
        } else {
            real_bind_addr = bind_addr;
        }

#ifdef ZMQ_HAVE_VXWORKS
        rc = bind (_fd, (sockaddr *) real_bind_addr->as_sockaddr (),
                   real_bind_addr->sockaddr_len ());
#else
        rc = bind (_fd, real_bind_addr->as_sockaddr (),
                   real_bind_addr->sockaddr_len ());

#endif
#ifdef ZMQ_HAVE_WINDOWS
        wsa_assert (rc != SOCKET_ERROR);
#else
        errno_assert (rc == 0);
#endif

        if (multicast) {
            const ip_addr_t *mcast_addr = udp_addr->target_addr ();

            if (mcast_addr->family () == AF_INET) {
                struct ip_mreq mreq;
                mreq.imr_multiaddr = mcast_addr->ipv4.sin_addr;
                mreq.imr_interface = bind_addr->ipv4.sin_addr;

                rc =
                  setsockopt (_fd, IPPROTO_IP, IP_ADD_MEMBERSHIP,
                              reinterpret_cast<char *> (&mreq), sizeof (mreq));

                errno_assert (rc == 0);
            } else if (mcast_addr->family () == AF_INET6) {
                struct ipv6_mreq mreq;
                int iface = _address->resolved.udp_addr->bind_if ();

                zmq_assert (iface >= -1);

                mreq.ipv6mr_multiaddr = mcast_addr->ipv6.sin6_addr;
                mreq.ipv6mr_interface = iface;

                rc =
                  setsockopt (_fd, IPPROTO_IPV6, IPV6_ADD_MEMBERSHIP,
                              reinterpret_cast<char *> (&mreq), sizeof (mreq));

                errno_assert (rc == 0);
            } else {
                //  Shouldn't happen
                abort ();
            }

#ifdef ZMQ_HAVE_WINDOWS
            wsa_assert (rc != SOCKET_ERROR);
#else
            errno_assert (rc == 0);
#endif
        }
        set_pollin (_handle);

        //  Call restart output to drop all join/leave commands
        restart_output ();
    }
}

void zmq::udp_engine_t::terminate ()
{
    zmq_assert (_plugged);
    _plugged = false;

    rm_fd (_handle);

    //  Disconnect from I/O threads poller object.
    io_object_t::unplug ();

    delete this;
}

void zmq::udp_engine_t::sockaddr_to_msg (zmq::msg_t *msg_, sockaddr_in *addr_)
{
    const char *const name = inet_ntoa (addr_->sin_addr);

    char port[6];
    sprintf (port, "%d", static_cast<int> (ntohs (addr_->sin_port)));

    const int size = static_cast<int> (strlen (name))
                     + static_cast<int> (strlen (port)) + 1
                     + 1; //  Colon + NULL
    const int rc = msg_->init_size (size);
    errno_assert (rc == 0);
    msg_->set_flags (msg_t::more);
    char *address = static_cast<char *> (msg_->data ());

    strcpy (address, name);
    strcat (address, ":");
    strcat (address, port);
}

int zmq::udp_engine_t::resolve_raw_address (char *name_, size_t length_)
{
    memset (&_raw_address, 0, sizeof _raw_address);

    const char *delimiter = NULL;

    // Find delimiter, cannot use memrchr as it is not supported on windows
    if (length_ != 0) {
        int chars_left = static_cast<int> (length_);
        char *current_char = name_ + length_;
        do {
            if (*(--current_char) == ':') {
                delimiter = current_char;
                break;
            }
        } while (--chars_left != 0);
    }

    if (!delimiter) {
        errno = EINVAL;
        return -1;
    }

    std::string addr_str (name_, delimiter - name_);
    std::string port_str (delimiter + 1, name_ + length_ - delimiter - 1);

    //  Parse the port number (0 is not a valid port).
    uint16_t port = static_cast<uint16_t> (atoi (port_str.c_str ()));
    if (port == 0) {
        errno = EINVAL;
        return -1;
    }

    _raw_address.sin_family = AF_INET;
    _raw_address.sin_port = htons (port);
    _raw_address.sin_addr.s_addr = inet_addr (addr_str.c_str ());

    if (_raw_address.sin_addr.s_addr == INADDR_NONE) {
        errno = EINVAL;
        return -1;
    }

    return 0;
}

void zmq::udp_engine_t::out_event ()
{
    msg_t group_msg;
    int rc = _session->pull_msg (&group_msg);
    errno_assert (rc == 0 || (rc == -1 && errno == EAGAIN));

    if (rc == 0) {
        msg_t body_msg;
        rc = _session->pull_msg (&body_msg);
        //  TODO rc is not checked here. We seem to assume rc == 0. An
        //  assertion should be added.

        const size_t group_size = group_msg.size ();
        const size_t body_size = body_msg.size ();
        size_t size;

        if (_options.raw_socket) {
            rc = resolve_raw_address (static_cast<char *> (group_msg.data ()),
                                      group_size);

            //  We discard the message if address is not valid
            if (rc != 0) {
                rc = group_msg.close ();
                errno_assert (rc == 0);

                body_msg.close ();
                errno_assert (rc == 0);

                return;
            }

            size = body_size;

            memcpy (_out_buffer, body_msg.data (), body_size);
        } else {
            size = group_size + body_size + 1;

            // TODO: check if larger than maximum size
            _out_buffer[0] = static_cast<unsigned char> (group_size);
            memcpy (_out_buffer + 1, group_msg.data (), group_size);
            memcpy (_out_buffer + 1 + group_size, body_msg.data (), body_size);
        }

        rc = group_msg.close ();
        errno_assert (rc == 0);

        body_msg.close ();
        errno_assert (rc == 0);

#ifdef ZMQ_HAVE_WINDOWS
        rc = sendto (_fd, _out_buffer, static_cast<int> (size), 0, _out_address,
                     static_cast<int> (_out_address_len));
        wsa_assert (rc != SOCKET_ERROR);
#elif defined ZMQ_HAVE_VXWORKS
        rc = sendto (_fd, reinterpret_cast<caddr_t> (_out_buffer), size, 0,
                     (sockaddr *) _out_address, (int) _out_address_len);
        errno_assert (rc != -1);
#else
        rc = sendto (_fd, _out_buffer, size, 0, _out_address, _out_address_len);
        errno_assert (rc != -1);
#endif
    } else
        reset_pollout (_handle);
}

const char *zmq::udp_engine_t::get_endpoint () const
{
    return "";
}

void zmq::udp_engine_t::restart_output ()
{
    //  If we don't support send we just drop all messages
    if (!_send_enabled) {
        msg_t msg;
        while (_session->pull_msg (&msg) == 0)
            msg.close ();
    } else {
        set_pollout (_handle);
        out_event ();
    }
}

void zmq::udp_engine_t::in_event ()
{
    sockaddr_storage in_address;
    socklen_t in_addrlen = sizeof (sockaddr_storage);
#ifdef ZMQ_HAVE_WINDOWS
    int nbytes =
      recvfrom (_fd, _in_buffer, MAX_UDP_MSG, 0,
                reinterpret_cast<sockaddr *> (&in_address), &in_addrlen);
    const int last_error = WSAGetLastError ();
    if (nbytes == SOCKET_ERROR) {
        wsa_assert (last_error == WSAENETDOWN || last_error == WSAENETRESET
                    || last_error == WSAEWOULDBLOCK);
        return;
    }
#elif defined ZMQ_HAVE_VXWORKS
    int nbytes = recvfrom (_fd, _in_buffer, MAX_UDP_MSG, 0,
                           (sockaddr *) &in_address, (int *) &in_addrlen);
    if (nbytes == -1) {
        errno_assert (errno != EBADF && errno != EFAULT && errno != ENOMEM
                      && errno != ENOTSOCK);
        return;
    }
#else
    int nbytes =
      recvfrom (_fd, _in_buffer, MAX_UDP_MSG, 0,
                reinterpret_cast<sockaddr *> (&in_address), &in_addrlen);
    if (nbytes == -1) {
#if !defined(TARGET_OS_IPHONE) || !TARGET_OS_IPHONE
        errno_assert (errno != EBADF && errno != EFAULT && errno != ENOMEM
                      && errno != ENOTSOCK);
#else
        errno_assert (errno != EBADF && errno != EFAULT && errno != ENOMEM
                      && errno != ENOTSOCK);
#endif
        return;
    }
#endif
    int rc;
    int body_size;
    int body_offset;
    msg_t msg;

    if (_options.raw_socket) {
        zmq_assert (in_address.ss_family == AF_INET);
        sockaddr_to_msg (&msg, reinterpret_cast<sockaddr_in *> (&in_address));

        body_size = nbytes;
        body_offset = 0;
    } else {
        // TODO in out_event, the group size is an *unsigned* char. what is
        // the maximum value?
        const char *group_buffer = _in_buffer + 1;
        const int group_size = _in_buffer[0];

        rc = msg.init_size (group_size);
        errno_assert (rc == 0);
        msg.set_flags (msg_t::more);
        memcpy (msg.data (), group_buffer, group_size);

        //  This doesn't fit, just ingore
        if (nbytes - 1 < group_size)
            return;

        body_size = nbytes - 1 - group_size;
        body_offset = 1 + group_size;
    }
    // Push group description to session
    rc = _session->push_msg (&msg);
    errno_assert (rc == 0 || (rc == -1 && errno == EAGAIN));

    //  Group description message doesn't fit in the pipe, drop
    if (rc != 0) {
        rc = msg.close ();
        errno_assert (rc == 0);

        reset_pollin (_handle);
        return;
    }

    rc = msg.close ();
    errno_assert (rc == 0);
    rc = msg.init_size (body_size);
    errno_assert (rc == 0);
    memcpy (msg.data (), _in_buffer + body_offset, body_size);

    // Push message body to session
    rc = _session->push_msg (&msg);
    // Message body doesn't fit in the pipe, drop and reset session state
    if (rc != 0) {
        rc = msg.close ();
        errno_assert (rc == 0);

        _session->reset ();
        reset_pollin (_handle);
        return;
    }

    rc = msg.close ();
    errno_assert (rc == 0);
    _session->flush ();
}

bool zmq::udp_engine_t::restart_input ()
{
    if (_recv_enabled) {
        set_pollin (_handle);
        in_event ();
    }

    return true;
}
