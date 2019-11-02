import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Snake, Msg, Control } from 'containers';

@connect(
    state => ({
        stage: state.app.stage
    })
)
export default class Stage extends Component {
    static propTypes = {
        stage: PropTypes.any,
    };

    constructor(...arg) {
        super(...arg);
    }

    render() {
        const { width, height, points } = this.props.stage;

        return (
            <div style={{
                width: width + 'px',
                height: height + 'px',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <Control />
                <Msg />
                <Snake />
                {
                    points.map(i => (
                        <div
                            key={i.id}
                            style={{
                                position: 'absolute',
                                left: i.x + 'px',
                                top: i.y + 'px',
                                width: i.width + 'px',
                                height: i.width + 'px',
                                backgroundColor: i.color,
                                borderRadius: '100px'
                            }}/>
                    ))
                }
            </div>
        );
    }
}
