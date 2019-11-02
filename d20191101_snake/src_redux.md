snake_package\src\redux\middleware

clientMiddleware.js
```js
import { message } from 'antd';
import { showLoading, hideLoading } from 'react-redux-loading-bar';

export default function clientMiddleware(client) {
    return ({ dispatch, getState }) => {
        return next => action => {
            if (typeof action === 'function') {
                return action(dispatch, getState);
            }

            const { promise, types, ...rest } = action;
            if (!promise) {
                return next(action);
            }

            const [REQUEST, SUCCESS, FAILURE] = types;
            next({ ...rest, type: REQUEST });
            next(showLoading());

            const actionPromise = promise(client);
            actionPromise.then(
                (result) => {
                    next(hideLoading());
                    return next({ ...rest, result, type: SUCCESS });
                },
                (error) => {
                    next(hideLoading());
                    message.error(error.msg);
                    return next({ ...rest, error, type: FAILURE });
                }
            ).catch((error) => {
                message.error('MIDDLEWARE ERROR:', error);
                next(hideLoading());
                return next({ ...rest, error, type: FAILURE });
            });

            return actionPromise;
        };
    };
}

```


snake_package\src\redux\modules

admin.js
```js
/**
 * Created by jiang on 2017/9/27.
 */
const CHANGE = 'admin/CHANGE';
const ADMINLIST = 'admin/ADMINLIST';
const ADMINLIST_SUCCESS = 'admin/ADMINLIST_SUCCESS';

const initialState = {
    adminList: [],
    selectedAdmin: '',
    loadingAdminList: false
};

export default function reducer(state = initialState, action = {}) {
    switch (action.type) {
        case CHANGE:
            return {
                ...state,
                ...action.arg
            };
        case ADMINLIST:
            return {
                ...state,
                loadingAdminList: true
            };
        case ADMINLIST_SUCCESS:
            return {
                ...state,
                adminList: action.result.allAdmin,
                selectedAdmin: state.selectedAdmin ? state.selectedAdmin : (action.result.allAdmin[0] ? action.result.allAdmin[0]._id : '')
            };
        default:
            return state;
    }
}

export const change = arg => ({ type: CHANGE, arg });

export const getAdminList = () => (dispatch, getState) => dispatch({
    types: [ADMINLIST, ADMINLIST_SUCCESS, ''],
    promise: (client) => client.get('/admin/all', { params: { _id: getState().auth.user._id } })
});

export const addAdmin = () => (dispatch, getState) => dispatch({
    types: ['', '', ''],
    promise: (client) => client.post('/admin/add', {
        data: {
            _id: getState().admin.selectedAdmin,
            selfId: getState().auth.user._id
        }
    })
});

```

app.js
```js
const CHANGE_USER_LIST = 'app/CHANGE_USER_LIST';
const CHANGE_STAGE = 'app/CHANGE_STAGE';
const SET_SOCKET = 'app/SET_SOCKET';

const initialState = {
    socket: null,
    snakes: {},
    stage: {
        width: 1920,
        height: 969,
        points: [],
        message: []
    }
};

export default function reducer(state = initialState, action = {}) {
    switch (action.type) {
        case CHANGE_USER_LIST:
            return {
                ...state,
                snakes: action.snakes
            };
        case CHANGE_STAGE:
            return {
                ...state,
                stage: action.stage
            };
        case SET_SOCKET:
            return {
                ...state,
                socket: action.socket
            };
        default:
            return state;
    }
}

export const changeUserList = snakes => ({
    type: CHANGE_USER_LIST,
    snakes
});

export const changeStage = stage => ({
    type: CHANGE_STAGE,
    stage
});

export const setSocket = socket => ({
    type: SET_SOCKET,
    socket
});

```

auth.js
```js
import { message } from 'antd';
import Cookies from 'js-cookie';

const LOAD = 'auth/LOAD';
const LOAD_SUCCESS = 'auth/LOAD_SUCCESS';
const LOAD_FAIL = 'auth/LOAD_FAIL';
const LOGIN = 'auth/LOGIN';
const LOGIN_SUCCESS = 'auth/LOGIN_SUCCESS';
const LOGIN_FAIL = 'auth/LOGIN_FAIL';
const LOGOUT = 'auth/LOGOUT';
const LOGOUT_SUCCESS = 'auth/LOGOUT_SUCCESS';
const LOGOUT_FAIL = 'auth/LOGOUT_FAIL';
const CHANGE = 'auth/CHANGE';
const REGISTER = 'auth/REGISTER';
const REGISTER_SUCCESS = 'auth/REGISTER_SUCCESS';

const initialState = {
    loaded: false,
    current: 'login'
};

export default function reducer(state = initialState, action = {}) {
    switch (action.type) {
        case LOAD:
            return {
                ...state,
                loading: true
            };
        case LOAD_SUCCESS:
            return {
                ...state,
                loading: false,
                loaded: true,
                user: action.result.user
            };
        case LOAD_FAIL:
            return {
                ...state,
                loading: false,
                loaded: false,
                error: action.error
            };
        case LOGIN:
            return {
                ...state,
                loggingIn: true,
                user: null
            };
        case LOGIN_SUCCESS:
            Cookies.set('token', action.result.token, { expires: 7 });

            return {
                ...state,
                loggingIn: false,
                user: action.result.user
            };
        case LOGIN_FAIL:
            return {
                ...state,
                loggingIn: false,
                user: null,
                loginError: action.error
            };
        case LOGOUT:
            return {
                ...state,
                loggingOut: true
            };
        case LOGOUT_SUCCESS:
            Cookies.remove('token');

            return {
                ...state,
                loggingOut: false,
                user: null
            };
        case LOGOUT_FAIL:
            return {
                ...state,
                loggingOut: false,
                logoutError: action.error
            };
        case CHANGE:
            return {
                ...state,
                ...action.arg
            };
        case REGISTER: {
            return {
                ...state,
                user: null
            };
        }
        case REGISTER_SUCCESS:
            Cookies.set('token', action.result.token, { expires: 7 });

            return {
                ...state,
                user: action.result.user
            };
        default:
            return state;
    }
}

export const change = arg => ({ type: CHANGE, arg });

export const isLoaded = globalState => globalState.auth && globalState.auth.loaded;

export const load = () => ({
    types: [LOAD, LOAD_SUCCESS, LOAD_FAIL],
    promise: (client) => client.get('admin/loadAuth')
});

export const login = () => (dispatch, getState) => {
    const { auth: { name, password } } = getState();

    if (!name || !password) {
        message.destroy();
        message.warning('请输入用户名，密码');
        return;
    }

    return dispatch({
        types: [LOGIN, LOGIN_SUCCESS, LOGIN_FAIL],
        promise: (client) => client.post('admin/login', { data: { name, password } })
    });
};

export const register = () => (dispatch, getState) => {
    const { auth: { name, password, againPassword } } = getState();

    if (!name || !password || !againPassword) {
        message.destroy();
        message.warning('请输入用户名，密码');
        return;
    }

    if (password !== againPassword) {
        message.destroy();
        message.warning('两次输入密码不一致');
        return;
    }

    return dispatch({
        types: [REGISTER, REGISTER_SUCCESS, ''],
        promise: (client) => client.post('admin/register', { data: { name, password } })
    });
};

export const logout = () => ({
    types: [LOGOUT, LOGOUT_SUCCESS, LOGOUT_FAIL],
    promise: (client) => client.get('admin/logout')
});

```

home.js
```js
/**
 * Created by jiang on 2017/9/16.
 */
const CHANGE = 'home/CHANGE';

const initialState = {
    currentKey: '1',
    openKeys: ['sub1'],
};

export default function reducer(state = initialState, action = {}) {
    switch (action.type) {
        case CHANGE:
            return {
                ...state,
                ...action.arg
            };
        default:
            return state;
    }
}

export const change = arg => ({ type: CHANGE, arg });

```

message.js
```js
/**
 * Created by jiang on 2017/9/16.
 */
import { message } from 'antd';

const CHANGE = 'message/CHANGE';
const LOAD_FRIENDS = 'message/LOAD_FRIENDS';
const CURRENT_MSG = 'message/CURRENT_MSG';
const CURRENT_MSG_LOADING = 'message/CURRENT_MSG_LOADING';

const initialState = {
    previewVisible: false,
    previewImageUrl: '',
    writeMsg: '',
    serverReceiveMsg: null,
    socketInit: false,
    socket: null,
    allMsg: {},
    loadFriends: false,
    friends: [],
    loadCurrentMsg: false,
    selectedFriend: {},
    onlineUsers: {},
    uploadQueue: {}
};

export default function reducer(state = initialState, action = {}) {
    switch (action.type) {
        case CHANGE:
            return {
                ...state,
                ...action.arg
            };
        case LOAD_FRIENDS:
            return {
                ...state,
                loadFriends: true,
                friends: action.result.friends,
                selectedFriend: state.selectedFriend._id ? state.selectedFriend : (action.result.friends[0] || {})
            };
        case CURRENT_MSG:
            state.allMsg[action.to] = action.result.messageList;

            return {
                ...state,
                allMsg: { ...state.allMsg },
                loadCurrentMsg: false
            };
        case CURRENT_MSG_LOADING:
            return {
                ...state,
                loadCurrentMsg: true
            };
        default:
            return state;
    }
}

export const change = arg => ({ type: CHANGE, arg });

export const loadFriends = () => (dispatch, getState) => {
    const isLoadFriends = getState().message.loadFriends;

    if (!isLoadFriends) {
        return dispatch({
            types: ['', LOAD_FRIENDS, ''],
            promise: (client) => client.get('/admin/list', { params: { _id: getState().auth.user._id } })
        });
    }

    return Promise.resolve();
};

export const loadMsg = () => (dispatch, getState) => {
    const {
        message: { selectedFriend, allMsg },
        auth: { user }
    } = getState();

    if (!allMsg[selectedFriend._id]) {
        return dispatch({
            types: [CURRENT_MSG_LOADING, CURRENT_MSG, ''],
            promise: (client) => client.get('/message/all', { params: { to: selectedFriend._id, come: user._id } }),
            to: selectedFriend._id
        });
    }

    return Promise.resolve();
};

export const sendMsg = () => (dispatch, getState) => {
    const {
        message: { writeMsg, allMsg, selectedFriend, onlineUsers, socket },
        auth: { user }
    } = getState();
    if (!socket) {
        message.warning('与服务器断开连接');
        return;
    }

    const msgObj = {
        come: user._id,
        to: selectedFriend._id,
        content: writeMsg
    };

    socket.emit('message', {
        id: onlineUsers[selectedFriend._id] ? onlineUsers[selectedFriend._id].socketId : '',
        message: msgObj
    });

    allMsg[selectedFriend._id].push(msgObj);
    dispatch(change({ allMsg: { ...allMsg }, writeMsg: '' }));
};

export const receiveMsg = (msg) => (dispatch, getState) => {
    const { allMsg } = getState().message;
    allMsg[msg.come].push(msg);
    dispatch(change({ allMsg: { ...allMsg } }));
};

export const socketReady = () => (dispatch, getState) => {
    const {
        message: { socket },
        auth: { user }
    } = getState();

    socket.emit('login', user);

    socket.on('onlineUsers', (onlineUsers) => {
        dispatch(change({ onlineUsers, socketInit: true }));
    });

    socket.on('message', (msg) => {
        dispatch(receiveMsg(msg));
    });
};

export const sendFileMsg = (fileInfo) => (dispatch, getState) => {
    const {
        message: { selectedFriend, onlineUsers, socket },
        auth: { user }
    } = getState();
    if (!socket) {
        message.warning('与服务器断开连接');
        return;
    }

    const msgObj = {
        come: user._id,
        to: selectedFriend._id,
        file: {
            name: fileInfo.file.name,
            path: user._id + '/' + fileInfo.file.name,
            size: fileInfo.file.size,
            type: fileInfo.file.type,
            creator: user._id
        },
        content: fileInfo.file.name
    };

    socket.emit('message', {
        id: onlineUsers[selectedFriend._id] ? onlineUsers[selectedFriend._id].socketId : '',
        message: msgObj
    });
};

export const changeFileMsg = (fileInfo) => (dispatch, getState) => {
    const {
        message: { selectedFriend, uploadQueue, allMsg },
        auth: { user }
    } = getState();

    if (uploadQueue[fileInfo.file.uid]) {
        allMsg[selectedFriend._id][uploadQueue[fileInfo.file.uid]] = {
            come: user._id,
            to: selectedFriend._id,
            fileInfo,
            path: user._id + '/' + fileInfo.file.name
        };
        dispatch(change({ allMsg: { ...allMsg } }));
    } else {
        uploadQueue[fileInfo.file.uid] = allMsg[selectedFriend._id].length;
        allMsg[selectedFriend._id].push({
            come: user._id,
            to: selectedFriend._id,
            fileInfo,
            path: user._id + '/' + fileInfo.file.name
        });
        dispatch(change({ allMsg: { ...allMsg }, uploadQueue: { ...uploadQueue } }));
    }
};

export const clearFileQueue = (fileInfo) => (dispatch, getState) => {
    const {
        message: { uploadQueue }
    } = getState();

    delete uploadQueue[fileInfo.file.uid];
    dispatch(change({ uploadQueue: { ...uploadQueue } }));
};

```

reducer.js
```js
import { combineReducers } from 'redux';
import { routerReducer as routing } from 'react-router-redux';
import { reducer as reduxAsyncConnect } from 'redux-async-connect';
import { loadingBarReducer as loadingBar } from 'react-redux-loading-bar';

import auth from './auth';
import home from './home';
import message from './message';
import admin from './admin';
import app from './app';

export default combineReducers({
    routing,
    loadingBar,
    reduxAsyncConnect,
    auth,
    home,
    message,
    admin,
    app
});

```



snake_package\src\redux\
create.js
```js
import { createStore as _createStore, applyMiddleware, compose } from 'redux';
import createMiddleware from './middleware/clientMiddleware';
import { routerMiddleware } from 'react-router-redux';
import thunk from 'redux-thunk';

export default function createStore(history, client, data) {
    // Sync dispatched route actions to the history
    const reduxRouterMiddleware = routerMiddleware(history);

    const middleware = [createMiddleware(client), reduxRouterMiddleware, thunk];

    let finalCreateStore;
    if (__DEVELOPMENT__ && __CLIENT__ && __DEVTOOLS__) {
        const { persistState } = require('redux-devtools');
        const DevTools = require('../containers/DevTools/DevTools');
        finalCreateStore = compose(
            applyMiddleware(...middleware),
            window.devToolsExtension ? window.devToolsExtension() : DevTools.instrument(),
            persistState(window.location.href.match(/[?&]debug_session=([^&]+)\b/))
        )(_createStore);
    } else {
        finalCreateStore = applyMiddleware(...middleware)(_createStore);
    }

    const reducer = require('./modules/reducer');
    const store = finalCreateStore(reducer, data);

    if (__DEVELOPMENT__ && module.hot) {
        module.hot.accept('./modules/reducer', () => {
            store.replaceReducer(require('./modules/reducer'));
        });
    }

    return store;
}

```
