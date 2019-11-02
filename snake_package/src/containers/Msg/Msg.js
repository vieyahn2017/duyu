import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Input } from 'antd';

@connect(
    state => ({
        stage: state.app.stage,
        socket: state.app.socket
    })
)
export default class Msg extends Component {
    static propTypes = {
        stage: PropTypes.any,
        socket: PropTypes.any
    };

    constructor(...arg) {
        super(...arg);
    }

    componentDidMount() {
        document.addEventListener('keydown', this._keyDown);
    }

    componentDidUpdate(prevProps) {
        const currentMsg = this.props.stage.message;
        const preMsg = prevProps.stage.message;
        if (preMsg.length && currentMsg.length && currentMsg[currentMsg.length - 1].id !== preMsg[preMsg.length - 1].id) {
            this.refs.msgContent.scrollTo(0, 99999999);
        }
    }

    componentWillUnmount() {
        document.removeEventListener('keydown', this._keyDown);
    }

    _keyDown = (e) => {
        if (e.keyCode === 13) {
            const value = this.refs.msg.refs.input.value;

            if (value) {
                this.props.socket.emit('message', value);
                this.refs.msg.refs.input.value = '';
            }
        }
    };

    render() {
        const { message } = this.props.stage;

        return (
            <div style={{
                width: '400px',
                height: '300px',
                position: 'absolute',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                right: '10px',
                bottom: '10px'
            }}>
                <div
                    ref="msgContent"
                    style={{
                        width: '100%',
                        height: '270px',
                        overflow: 'auto'
                    }}>
                    {
                        message.map(i => (
                            <p key={i.id} style={{ color: '#eee', padding: '8px', opacity: '0.7' }}>
                                <span style={{ fontWeight: 'bold', color: 'orange', paddingRight: '5px 10px' }}>{
                                    '[' + i.from + ']:'
                                }</span>
                                {i.content}
                            </p>
                        ))
                    }
                </div>
                <Input
                    style={{ opacity: '0.7', marginTop: '10px', background: 'none', color: '#eee', border: '1px solid #666' }}
                    ref="msg"
                    className="login-input"
                />
            </div>
        );
    }
}
