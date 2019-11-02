import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import io from 'socket.io-client';
import * as _actions from 'redux/modules/app';
import Cookies from 'js-cookie';
import { Stage } from 'containers';

@connect(
    state => ({
        user: state.auth.user,
        socket: state.app.socket
    }),
    dispatch => ({ actions: bindActionCreators(_actions, dispatch) }),
)
export default class Container extends Component {
    static propTypes = {
        socket: PropTypes.any,
        user: PropTypes.object,
        actions: PropTypes.object
    };

    constructor(...arg) {
        super(...arg);

        this.keyCode = '';
    }

    componentDidMount() {
        this.initSocket();
    }

    componentWillUnmount() {
        if (this.props.socket && this.props.socket.destroy) this.props.socket.destroy();
    }

    initSocket = () => {
        const socket = io('', { path: '/ws' });

        socket.on('connect', () => {
            socket
                .emit('authenticate', { token: Cookies.get('token') })
                .on('authenticated', () => {
                    this.props.actions.setSocket(socket);
                    socket.emit('login', this.props.user);
                })
                .on('unauthorized', msg => {
                    console.log(msg);
                })
                .on('loop', ({ snakes, stage }) => {
                    this.props.actions.changeUserList(snakes);
                    this.props.actions.changeStage(stage);

                    socket.emit('ok', this.keyCode);
                    this.keyCode = '';
                });
        });

        document.addEventListener('keydown', e => this.keyCode = e.keyCode);
    };

    render() {
        return (
            <div id="app-container">
                <Stage/>
            </div>
        );
    }
}
