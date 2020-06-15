import { Reducer } from 'redux';
import { FETCH_USER, FETCH_USER_SUCCESS, FETCH_USER_FAILURE, FetchUserSuccessAction } from '../actions/user';
import { UserState } from '../types';

const initialState: UserState = {
    fetching: false,
    created: null,
    isAdmin: false,
    lastActivity: null,
    name: 'Anonymous',
    isAnonymous: true,
};

const user: Reducer = (state = initialState, action) => {
    switch(action.type) {
        case FETCH_USER:
            return {...state, fetching: true};
        case FETCH_USER_SUCCESS:
            return {
                ...state,
                fetching: false,
                ...(action as FetchUserSuccessAction).user,
                isAnonymous: false
            };
        case FETCH_USER_FAILURE:
            return {...state, ...initialState};
        default:
            return state;
    }
}

export default user;