import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

@connect(
    state => ({
        snakes: state.app.snakes
    })
)
export default class Snake extends Component {
    static propTypes = {
        snakes: PropTypes.any,
    };

    constructor(...arg) {
        super(...arg);
    }

    render() {
        const _snakes = [];
        const keys = Object.keys(this.props.snakes);

        keys.forEach(i => {
            _snakes.push(this.props.snakes[i]);

        });

        return (
            <div>
                {
                    _snakes.map(i => (
                        <div key={i.id}>
                            {
                                i.bodys.map((j, index) => {
                                    if (index === 0) {
                                        return (
                                            <div
                                                className="snake-body"
                                                key={i.id + j.id}
                                                style={{
                                                    boxShadow: `rgba(${i.rgb[0] + 50}, ${i.rgb[1] + 50}, ${i.rgb[2] + 50}, 1) 0 0 ${i.lv + 9}px`,
                                                    position: 'absolute',
                                                    left: j.x + 'px',
                                                    top: j.y + 'px',
                                                    backgroundColor: i.color,
                                                    width: j.width + 'px',
                                                    height: j.width + 'px',
                                                    outline: i.color + ' dotted thick',
                                                    zIndex: '99999',
                                                }}
                                            >
                                                <div className="tooltip">
                                                    <span>
                                                        <span style={{
                                                            fontWeight: 'bold',
                                                            color: i.color
                                                        }}>{i.user.name}</span>
                                                        {' '}
                                                        <span
                                                            style={{
                                                                fontWeight: 'bold',
                                                                color: 'orange'
                                                            }}>{`[ ${i.lv} ][ ${i.weight} ]`}
                                                        </span>
                                                    </span>
                                                </div>
                                            </div>
                                        );
                                    }

                                    return (<div
                                        className="snake-body"
                                        key={i.id + j.id}
                                        style={{
                                            boxShadow: `rgba(${i.rgb[0] + 50}, ${i.rgb[1] + 50}, ${i.rgb[2] + 50}, 1) 0 0 ${i.lv + 9}px`,
                                            position: 'absolute',
                                            left: j.x + 'px',
                                            top: j.y + 'px',
                                            backgroundColor: i.color,
                                            width: j.width + 'px',
                                            height: j.width + 'px'
                                        }}
                                    />);
                                })
                            }
                        </div>
                    ))
                }
            </div>
        );
    }
}
