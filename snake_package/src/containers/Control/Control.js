import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Button } from 'antd';

@connect(
    state => ({
        socket: state.app.socket
    })
)
export default class Msg extends Component {
    static propTypes = {
        socket: PropTypes.any
    };

    constructor(...arg) {
        super(...arg);
    }


    onlineSnake = () => {
        this.props.socket.emit('online');
    };

    offlineSnake = () => {
        this.props.socket.emit('offline');
    };

    resetSnake = () => {
        this.props.socket.emit('reset');
    };

    render() {

        return (
            <div style={{
                position: 'absolute',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                opacity: '0.7',
                left: '10px',
                top: '10px'
            }}>
                <Button onClick={this.resetSnake}>换肤</Button>
                <Button onClick={this.offlineSnake}>存档下线</Button>
                <Button onClick={this.onlineSnake}>删档上线</Button>
            </div>
        );
    }
}
