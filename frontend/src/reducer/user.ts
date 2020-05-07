import { Reducer } from 'redux';

const initialState = {};

const user: Reducer = (state = initialState, action) => {
    switch(action.type) {
        case 'FOO':
            return state;
        default:
            return state;
    }
}

export default user;