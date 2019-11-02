snake_package\src\containers


index.js
```js
export App from './App/App';
export AddAdmin from './AddAdmin/AddAdmin';

export Chat from './Chat/Chat';
export Container from './Container/Container';
export Control from './Control/Control';

export Home from './Home/Home';

export Login from './Login/Login';

export Msg from './Msg/Msg';

export NotFound from './NotFound/NotFound';

export Stage from './Stage/Stage';
export Snake from './Snake/Snake';

export WebGlStage from './WebGlStage/WebGlStage';

```


AddAdmin/
App/
Chat/
Container/
Control/
DevTools/
Home/
Login/
Msg/
NotFound/
Snake/
Stage/
WebGlStage/



AddAdmin/
AddAdmin.js
```js
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { getAdminList, change, addAdmin } from 'redux/modules/admin';
import { change as changeFriendsList, loadFriends } from 'redux/modules/message';
import { Select, Button } from 'antd';
import './AddAdmin.scss';
const Option = Select.Option;

@connect(state => ({
    adminList: state.admin.adminList,
    selectedAdmin: state.admin.selectedAdmin
}), {
    getAdminList,
    change,
    addAdmin,
    changeFriendsList,
    loadFriends
})
export default class AddAdmin extends Component {
    static propTypes = {
        adminList: PropTypes.array,
        selectedAdmin: PropTypes.string,
        change: PropTypes.func,
        getAdminList: PropTypes.func,
        addAdmin: PropTypes.func,
        loadFriends: PropTypes.func,
        changeFriendsList: PropTypes.func
    };

    componentDidMount() {
        this.props.getAdminList();
    }

    render() {
        const { adminList, selectedAdmin } = this.props;
        return (
            <div className="add-admin-content">
                <Select
                    value={selectedAdmin}
                    showSearch
                    style={{ width: 200 }}
                    placeholder="选择你想添加的好友"
                    optionFilterProp="children"
                    onChange={(e) => {
                        this.props.change({ selectedAdmin: e });
                    }}
                >
                    {adminList.map((item, i) => <Option key={i} value={item._id}>{item.name}</Option>)}
                </Select>
                <Button
                    onClick={() => {
                        this.props.addAdmin()
                            .then(() => {
                                this.props.change({ selectedAdmin: '' });
                                this.props.getAdminList();
                                this.props.changeFriendsList({ loadFriends: false });
                                this.props.loadFriends();
                            });
                    }}
                    style={{ marginLeft: '16px' }} type="primary"
                    icon="plus"
                >添加</Button>
            </div>
        );
    }
}

```

AddAdmin.scss
```scss
.add-admin-content {
  padding: 6px;
}
```

App/
App.js
```js
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { asyncConnect } from 'redux-async-connect';
import Helmet from 'react-helmet';
import { push } from 'react-router-redux';
import './App.scss';
import LoadingBar from 'react-redux-loading-bar';
import { isLoaded as isAuthLoaded, load as loadAuth } from 'redux/modules/auth';

@asyncConnect([{
    promise: ({ store: { dispatch, getState } }) => {
        const promises = [];

        if (!isAuthLoaded(getState())) {
            promises.push(dispatch(loadAuth()));
        }

        return Promise.all(promises);
    }
}])
@connect(state => ({ user: state.auth.user }), { pushState: push })
export default class App extends Component {
    static propTypes = {
        children: PropTypes.object,
        user: PropTypes.object,
        pushState: PropTypes.func
    };

    static contextTypes = {
        store: PropTypes.object.isRequired
    };

    componentWillReceiveProps(nextProps) {
        if (!this.props.user && nextProps.user) {
            this.props.pushState('/home');
        } else if (this.props.user && !nextProps.user) {
            this.props.pushState('/');
        }
    }

    render() {
        return (
            <div className="app">
                <Helmet title="dog" />
                <LoadingBar
                    style={{
                        backgroundColor: '#108ee9',
                        zIndex: 99999,
                        height: '2px',
                        position: 'fixed',
                        top: '0',
                        left: '0'
                    }}
                />
                {this.props.children}
            </div>
        );
    }
}

```

App.scss
```scss
@import "../../theme/variables.css";

#content {
  height: 100%;
}

.app {
  height: 100%;
}

#app-container {
  height: 100%;
  width: 100%;
  overflow: auto;
}

body {
  background-color: #111;
}

.tooltip {
  position: absolute;
  padding: 1px 6px;
  border-radius: 2px;
  background-color: #fff;
  left: -10px;
  top: -28px;
  opacity: 0.7;
  color: #111;
  white-space: nowrap;
}

.snake-body {
  //box-shadow: #fff 0px 0px 10px;
}

```


Chat/

Chat.js
```js
/**
 * Created by jiang on 2017/9/17.
 */
import React from 'react';
import FriendsList from './FriendsList/FriendsList';
import MsgList from './MsgList/MsgList';
import './Chat.scss';

export default () => (
    <div className="friends">
        <FriendsList />
        <MsgList />
    </div>
);

```

Chat.scss
```scss
.friends {
  height: 100%;
}

```

Chat/FriendsList/
FriendsList.js
```js
/**
 * Created by jiang on 2017/9/17.
 */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { loadMsg, change } from 'redux/modules/message';
import { Avatar } from 'antd';
import './FriendsList.scss';

@connect(state => ({
    user: state.auth.user,
    friends: state.message.friends,
    onlineUsers: state.message.onlineUsers,
    selectedFriend: state.message.selectedFriend,
}), { change, loadMsg })
export default class FriendsList extends Component {
    static propTypes = {
        user: PropTypes.object,
        friends: PropTypes.array,
        change: PropTypes.func,
        onlineUsers: PropTypes.object,
        selectedFriend: PropTypes.object,
        loadMsg: PropTypes.func,
    };

    render() {
        const { friends, selectedFriend, onlineUsers }  = this.props;
        return (
            <div className="friends-left">
                {
                    friends.map((item, i) => (
                        <div
                            key={i}
                            className={item._id === selectedFriend._id ? 'friends-line friends-checked' : 'friends-line'}
                            onClick={() => {
                                this.props.change({ selectedFriend: item });
                                this.props.loadMsg();
                            }}
                        >
                            {
                                item.avatar &&
                                <Avatar src={item.avatar.path} />
                            }
                            {
                                !item.avatar &&
                                <Avatar
                                    style={{
                                        backgroundColor: onlineUsers[item._id] ? '#108ee9' : '#ddd'
                                    }}
                                >{item.name}
                                </Avatar>
                            }
                            {'   ' + item.name}
                        </div>
                    ))
                }
            </div>
        );
    }
}

```

FriendsList.scss
```scss
.friends-left {
  float: left;
  width: 120px;
}

.friends-line {
  padding: 5px;
  cursor: pointer;
  transition: all 1s;
}

.friends-checked {
  background-color: #ecf6fd;
}

.friends-line:hover {
  background-color: #ecf6fd;
}

.friends-line .ant-avatar {
  vertical-align: middle;
}

```


Chat/MsgList/
MsgList.js
```js
/**
 * Created by jiang on 2017/9/18.
 */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Upload, Modal } from 'antd';
import { change } from 'redux/modules/message';
import WriteMsg from '../WriteMsg/WriteMsg';
import './MsgList.scss';

@connect(state => ({
    user: state.auth.user,
    selectedFriend: state.message.selectedFriend,
    allMsg: state.message.allMsg,
    previewVisible: state.message.previewVisible,
    previewImageUrl: state.message.previewImageUrl,
}), { change })
export default class MsgList extends Component {
    static propTypes = {
        user: PropTypes.object,
        allMsg: PropTypes.object,
        selectedFriend: PropTypes.object,
        change: PropTypes.func,
        previewImageUrl: PropTypes.any,
        previewVisible: PropTypes.bool,
    };

    componentDidMount() {
        this.gotoBottom();
    }

    componentDidUpdate(preProps) {
        if (preProps.selectedFriend !== this.props.selectedFriend || preProps.allMsg !== this.props.allMsg) this.gotoBottom();
    }

    gotoBottom = () => {
        const ele = document.querySelectorAll('.message-line');
        if (ele.length > 0) ele[ele.length - 1].scrollIntoView();
    };

    typeRenderMsg = (msg, i) => {
        if (msg.fileInfo) {
            return (
                <Upload
                    onPreview={() => {
                        this.props.change({ previewVisible: true, previewImageUrl: msg.path });
                    }}
                    onRemove={false}
                    action=""
                    listType="picture-card"
                    fileList={[msg.fileInfo.file]}
                />
            );
        }

        if (msg.file && msg.file.type.indexOf('image') > -1) {
            return (<Upload
                onPreview={() => {
                    this.props.change({ previewVisible: true, previewImageUrl: msg.file.path });
                }}
                onRemove={false}
                action=""
                listType="picture-card"
                fileList={[{
                    uid: i,
                    name: '',
                    status: 'done',
                    url: msg.file.path,
                }]}
            />);
        }

        if (msg.file) {
            return (<a download={msg.file.name} href={msg.file.path}>{msg.content}</a>);
        }

        return msg.content;
    };

    render() {
        const {
            allMsg,
            selectedFriend,
            user,
            previewVisible,
            previewImageUrl,
        } = this.props;

        return (
            <div className="friends-right">
                <div className="friends-message">
                    {
                        (allMsg[selectedFriend._id] || []).map((item, i) => {
                            return (
                                <div className="message-line" key={i}>
                                    <div className={item.come === (user || {})._id
                                        ? 'message-left' : 'message-right'}>
                                        {this.typeRenderMsg(item, i)}
                                    </div>
                                </div>
                            );
                        })
                    }
                </div>
                <Modal
                    width={800}
                    visible={previewVisible}
                    footer={null}
                    onCancel={() => {
                        this.props.change({ previewVisible: false });
                    }}>
                    <img
                        style={{ width: '100%' }}
                        src={previewImageUrl}
                    />
                </Modal>
                <WriteMsg />
            </div>
        );
    }
}

```

MsgList.scss
```scss
.friends-right {
  margin-left: 120px;
  border-left: 1px solid #e9e9e9;
  height: 100%;
  position: relative;
}

.friends-message {
  height: calc(100% - 110px);
  overflow: auto;
  width: 100%;
}

.friends-tool {
  position: absolute;
  bottom: 0px;
  left: 0px;
  width: 100%;
  height: 110px;
}

.friends-img {
  height: 28px;
  line-height: 28px;
  color: #666;
  padding-left: 10px;
  border-top: 1px solid #e9e9e9;
}

.friends-send {
  border-top: 1px solid #e9e9e9;
}

.friends-send textarea {
  width: 100%;
  height: 79px;
  border: none;
  margin: 0px;
  padding: 6px;
  outline: none;
}

.message-line {
  overflow: hidden;
}

.message-left {
  max-width: 90%;
  color: #666;
  padding: 4px;
  float: left;
  margin-top: 2px;
  margin-bottom: 4px;
  margin-left: 4px;
  border-radius: 4px;
  border: 1px solid #e9e9e9;
}

.message-right {
  max-width: 90%;
  color: #666;
  padding: 4px;
  float: right;
  margin-top: 2px;
  margin-bottom: 4px;
  margin-right: 4px;
  border-radius: 4px;
  border: 1px solid #e9e9e9;
}

.message-line .ant-upload-list-picture-card .ant-upload-list-item {
  margin-right: 0px;
  margin-bottom: 0px;
}

.message-line .ant-upload-list-picture-card .ant-upload-list-item {
  border: none;
}
```


Chat/WriteMsg/
WriteMsg.js
```js
/**
 * Created by jiang on 2017/9/18.
 */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { change, sendMsg, sendFileMsg, changeFileMsg, clearFileQueue } from 'redux/modules/message';
import { Upload, Icon, Input } from 'antd';
const { TextArea } = Input;
import './WriteMsg.scss';

@connect(state => ({
    writeMsg: state.message.writeMsg,
    loadCurrentMsg: state.message.loadCurrentMsg,
    socketInit: state.message.socketInit
}), { change, sendMsg, sendFileMsg, clearFileQueue, changeFileMsg })
export default class WriteMsg extends Component {
    static propTypes = {
        writeMsg: PropTypes.any,
        change: PropTypes.func,
        sendMsg: PropTypes.func,
        loadCurrentMsg: PropTypes.bool,
        socketInit: PropTypes.bool,
        sendFileMsg: PropTypes.func,
        changeFileMsg: PropTypes.func,
        clearFileQueue: PropTypes.func
    };

    render() {
        return (
            <div className="friends-tool">
                <div className="friends-img">
                    {!this.props.socketInit &&
                    <span className="socket-loading"><Icon type="loading" />  连接聊天服务器...</span>}
                    <Upload
                        name="file"
                        action="/api/uploads"
                        showUploadList={false}
                        onChange={(fileInfo) => {
                            this.props.changeFileMsg(fileInfo);
                            if (fileInfo.file.status === 'done') {
                                this.props.clearFileQueue(fileInfo);
                                this.props.sendFileMsg(fileInfo);
                            }
                        }}
                    >
                        <a><Icon type="upload" /> 上传文件</a>
                    </Upload>
                </div>
                <div className="friends-send">
            <TextArea
                disabled={this.props.loadCurrentMsg || !this.props.socketInit}
                value={this.props.writeMsg}
                onChange={(e) => {
                    this.props.change({ writeMsg: e.target.value });
                }}
                onKeyDown={(e) => {
                    if (e.keyCode === 13) this.props.sendMsg();
                }}
            />
                </div>
            </div>
        );
    }
}

```

WriteMsg.scss
```scss
.socket-loading {
  margin: 0px 12px;
  color: #ff571a;
}

.friends-send textarea:focus {
  border: none !important;
  box-shadow: none !important;
}
```


Container/
Container.js
```js
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

```

Control/
Control.js
```js
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
            </div>
        );
    }
}

```

DevTools/
DevTools.js
```js
import React from 'react';
import { createDevTools } from 'redux-devtools';
import LogMonitor from 'redux-devtools-log-monitor';
import DockMonitor from 'redux-devtools-dock-monitor';

export default createDevTools(
    <DockMonitor
        defaultIsVisible={false}
        toggleVisibilityKey="ctrl-H"
        changePositionKey="ctrl-Q"
    >
        <LogMonitor />
    </DockMonitor>
);

```

Home/
Home.js
```js
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import Helmet from 'react-helmet';
import { Menu, Icon, Avatar, Button } from 'antd';
import io from 'socket.io-client';
import { Chat, AddAdmin } from 'containers';
import Cookies from 'js-cookie';
// import { , ChatAdmin, AddGroup, JoinGroup } from 'containers';
const SubMenu = Menu.SubMenu;
import './Home.scss';

import { logout } from 'redux/modules/auth';
import { change } from 'redux/modules/home';
import { change as changeMsg, receiveMsg, loadFriends, loadMsg, socketReady } from 'redux/modules/message';

@connect(state => ({
    socket: state.message.socket,
    user: state.auth.user,
    home: state.home,
}), { logout, change, changeMsg, receiveMsg, loadFriends, loadMsg, socketReady })
export default class Home extends Component {
    static propTypes = {
        user: PropTypes.object,
        home: PropTypes.object,
        logout: PropTypes.func,
        change: PropTypes.func,
        changeMsg: PropTypes.func,
        receiveMsg: PropTypes.func,
        loadFriends: PropTypes.func,
        loadMsg: PropTypes.func,
        socketReady: PropTypes.func,
        socket: PropTypes.any
    };

    componentDidMount() {
        this.props.loadFriends().then(this.props.loadMsg);

        const socket = io('', { path: '/ws' });

        socket.on('connect', () => {
            socket
                .emit('authenticate', { token: Cookies.get('token') })
                .on('authenticated', () => {
                    this.props.changeMsg({ socketInit: true, socket });
                    this.props.socketReady();
                })
                .on('unauthorized', (msg) => {
                    console.log(msg);
                    this.props.changeMsg({ socketInit: false, socket: null });
                });
        });
    }

    componentWillUnmount() {
        if (this.props.socket && this.props.socket.destroy) this.props.socket.destroy();
        this.props.changeMsg({ socketInit: false, socket: null });
    }

    renderTop = () => {
        const { user } = this.props;
        const { avatar, name } = user || {};
        return (
            <div className="home-top">
                {avatar &&
                <Avatar
                    src={avatar.path}
                    style={{ marginLeft: '18px', marginTop: '4px' }}
                />}
                {!avatar &&
                <Avatar
                    style={{
                        backgroundColor: '#108ee9',
                        marginLeft: '18px', marginTop: '4px'
                    }}
                >{name}</Avatar>}
                <Button
                    onClick={() => {
                        this.props.logout().then(() => {
                            window.location.reload();
                        });
                    }}
                    style={{ float: 'right', marginRight: '18px', marginTop: '8px' }} shape="circle" icon="logout"
                    size="small" />
            </div>
        );
    };

    renderLeft = () => {
        const { home } = this.props;
        return (
            <div className="home-left">
                <Menu
                    openKeys={home.openKeys}
                    selectedKeys={[home.currentKey]}
                    onClick={(e) => this.props.change({ currentKey: e.key })}
                    onOpenChange={(e) => this.props.change({ openKeys: e })}
                    mode="inline"
                >
                    <SubMenu key="sub1" title={<span><Icon type="user" /><span>朋友</span></span>}>
                        <Menu.Item key="1">朋友聊天</Menu.Item>
                        <Menu.Item key="2">添加朋友</Menu.Item>
                        <Menu.Item key="3">删除朋友</Menu.Item>
                    </SubMenu>
                    <SubMenu key="sub2" title={<span><Icon type="team" /><span>群组</span></span>}>
                        <Menu.Item key="4">群组聊天</Menu.Item>
                        <Menu.Item key="5">创建群组</Menu.Item>
                        <Menu.Item key="6">加入群组</Menu.Item>
                        <Menu.Item key="7">删除群组</Menu.Item>
                    </SubMenu>
                    <SubMenu key="sub4" title={<span><Icon type="setting" /><span>个人中心</span></span>}>
                        <Menu.Item key="8">修改个人信息</Menu.Item>
                    </SubMenu>
                </Menu>
            </div>
        );
    };

    renderRight = () => {
        const keys = {
            1: <Chat />,
            2: <AddAdmin />,
            // 5: <AddGroup />,
            // 6: <JoinGroup />
        };

        return (
            <div className="home-right">
                {keys[this.props.home.currentKey] || '组件暂无，敬请期待'}
            </div>
        );
    };

    render() {
        return (
            <div className="j-home">
                <Helmet title="Home" />
                { this.renderTop() }
                { this.renderLeft() }
                { this.renderRight() }
            </div>
        );
    }
}



```

Home.scss
```scss
.home-top {
  height: 40px;
  border-bottom: 1px solid #e9e9e9;
}

.home-left {
  width: 180px;
  float: left;
  height: calc(100% - 40px);
}

.home-right {
  margin-left: 180px;
  height: calc(100% - 40px);
}

.j-home {
  height: 100%;
}

.j-home .ant-menu-inline {
  height: 100%;
}
```


Login/
Login.js
```js
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import Helmet from 'react-helmet';
import './Login.scss';
import { ThreeBg } from 'components';
import { Button, Input } from 'antd';
import { connect } from 'react-redux';
import * as loginActions from 'redux/modules/auth';

@connect(state => ({ auth: state.auth }), loginActions)
export default class Login extends Component {
    static propTypes = {
        auth: PropTypes.object,
        login: PropTypes.func,
        change: PropTypes.func,
        register: PropTypes.func
    };

    constructor(...arg) {
        super(...arg);
    }

    componentDidMount() {
        document.addEventListener('keydown', this._keyDown);
    }

    componentWillUnmount() {
        document.removeEventListener('keydown', this._keyDown);
    }

    _keyDown = (e) => {
        if (e.keyCode === 13) this.props.login();
    };

    render() {
        const { auth } = this.props;
        return (
            <div>
                <Helmet title="dog-login" />
                <ThreeBg
                    style={{ position: 'absolute' }}
                />
                <div
                    className="login-center-content"
                    style={{
                        opacity: auth.current === 'login' ? 0.6 : 0,
                        zIndex: auth.current === 'login' ? 101 : 99
                    }}
                >
                    <Input
                        value={auth.name}
                        onChange={(e) => {
                            this.props.change({ name: e.target.value });
                        }}
                        className="login-input"
                        placeholder="用户名"
                    />
                    <Input
                        value={auth.password}
                        onChange={(e) => {
                            this.props.change({ password: e.target.value });
                        }}
                        className="login-input"
                        placeholder="密码"
                        type="password"
                    />
                    <Button
                        style={{ width: '100%', marginBottom: '20px' }}
                        type={'primary'}
                        onClick={this.props.login}
                    >登录</Button>
                    <a
                        onClick={(e) => {
                            e.preventDefault();
                            this.props.change({ current: 'register' });
                        }}
                    >去注册</a>
                </div>
                <div
                    className="login-center-content"
                    style={{
                        opacity: auth.current === 'register' ? 0.6 : 0,
                        zIndex: auth.current === 'register' ? 101 : 99
                    }}
                >
                    <Input
                        value={auth.name}
                        onChange={(e) => {
                            this.props.change({ name: e.target.value });
                        }}
                        className="login-input"
                        placeholder="用户名"
                    />
                    <Input
                        value={auth.password}
                        onChange={(e) => {
                            this.props.change({ password: e.target.value });
                        }}
                        className="login-input"
                        placeholder="密码"
                        type="password"
                    />
                    <Input
                        value={auth.againPassword}
                        onChange={(e) => {
                            this.props.change({ againPassword: e.target.value });
                        }}
                        className="login-input"
                        placeholder="再次输入密码"
                        type="password"
                    />
                    <Button
                        style={{ width: '100%', marginBottom: '20px' }}
                        type={'primary'}
                        onClick={this.props.register}
                    >注册</Button>
                    <a
                        onClick={(e) => {
                            e.preventDefault();
                            this.props.change({ current: 'login' });
                        }}
                    >去登录</a>
                </div>
            </div>
        );
    }
}

```

Login.scss
```scss
.login-center-content {
  width: 500px;
  height: 300px;
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  margin: auto;
  z-index: 100;
  transition: all 1s;
  padding: 10px;
}

.login-input {
  margin-bottom: 40px;
}
```


Msg/
Msg.js
```js
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

```

NotFound/
NotFound.js
```js
import React from 'react';

export default () => (
    <div className="container">
        <h1> 404 </h1>
    </div>
);

```

Snake/
Snake.js
```js
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


```

Stage/
Stage.js
```js
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

```

WebGlStage/
WebGlStage.js
```js
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
            width: 1920,
            height: 900,
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

                    for (const key in points) {
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

```


