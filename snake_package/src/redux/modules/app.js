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
