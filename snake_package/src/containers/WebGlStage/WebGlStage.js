import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import * as THREE from 'three';
import io from 'socket.io-client';
import Cookies from 'js-cookie';
import Stats from '../../lib/stats.module';
import ByteBuffer from 'bytebuffer';

@connect(
    state => ({
        user: state.auth.user,
    })
)
export default class WebGlStage extends Component {
    static propTypes = {
        user: PropTypes.object,
        actions: PropTypes.object
    };

    constructor(...arg) {
        super(...arg);

        this.stage = {
            width: 1440,
            height: 600,
            points: [],
            message: [],
        };
        this.meshs = {};
        this.points = {};
    }

    componentDidMount() {
        window.THREE = THREE;

        this.init();
        this.animate();
        this.initSocket();
    }

    componentWillUnmount() {
        cancelAnimationFrame(this.time);
        THREE.Cache.clear();
    }

    initSocket = () => {
        const socket = io('', { path: '/ws' });

        socket.on('connect', () => {
            socket
                .emit('authenticate', { token: Cookies.get('token') })
                .on('authenticated', () => {
                    socket.emit('login', this.props.user);
                })
                .on('unauthorized', msg => {
                    console.log(msg);
                })
                .on('stage', msg => {
                    this.stage = msg;
                    // this.props.actions.changeStage(msg);
                })
                // .on('loop', msg => {
                //
                // })
                .on('points', _points => {
                    const points = JSON.parse(ByteBuffer.wrap(_points.buffer).readIString());

                    for (const key of points) {
                        const point = points[key];

                        if (this.meshs[key]) {
                            this.meshs[key].position.x = point.x;
                            this.meshs[key].position.y = -point.y;
                        } else {
                            const geometry = new THREE.BoxGeometry(point.width, point.width, point.width);
                            const material = new THREE.MeshBasicMaterial({ color: point.color });
                            const cube = new THREE.Mesh(geometry, material);
                            cube.position.x = point.x;
                            cube.position.y = -point.y;

                            this.scene.add(cube);
                            this.meshs[key] = cube;
                        }
                    }

                    for (const key in this.meshs) {
                        if (!points[key]) {
                            const mesh = this.meshs[key];
                            this.scene.remove(mesh);
                            delete  this.meshs[key];
                        }
                    }
                });
        });

        document.addEventListener('keydown', e => socket.emit('control', e.keyCode));
    };

    init = () => {
        const width = 1920;
        const height = 900;
        this.stats = new Stats();

        this.container = document.getElementById('web-gl-stage');
        this.camera = new THREE.PerspectiveCamera(70, width / height, 0.1, 1000);
        this.scene = new THREE.Scene();
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(width, height);
        this.container.appendChild(this.renderer.domElement);
        this.container.appendChild(this.stats.dom);
        this.camera.position.z = 1400;
        this.camera.position.x = 1000;
        this.camera.position.y = -1000;
    };

    animate = () => {
        this.time = requestAnimationFrame(this.animate);

        this.stats.update();

        this.renderer.render(this.scene, this.camera);
    };

    render() {
        return (
            <div id="web-gl-stage" style={{ height: '100%' }}/>
        );
    }
}
