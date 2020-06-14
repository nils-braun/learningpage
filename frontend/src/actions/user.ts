import { Action } from "redux";

import { AppThunk, UserApi } from "../types";
import { getUserLink, fetchWrapper } from "../utils";

export const FETCH_USER = 'FETCH_USER';
export interface FetchUserAction extends Action {};
const fetchUser = (): FetchUserAction => {
    return {
        type: FETCH_USER,
    };
}

export const FETCH_USER_SUCCESS = 'FETCH_USER_SUCCESS';
export interface FetchUserSuccessAction extends Action {
    user: UserApi
}
const fetchUserSuccess = (user: UserApi): FetchUserSuccessAction => {
    return {
        type: FETCH_USER_SUCCESS,
        user
    };
}

export const FETCH_USER_FAILURE = 'FETCH_USER_FAILURE';
const fetchUserFailure = (): Action => {
    return {
        type: FETCH_USER_FAILURE
    };
}
export const thunkFetchUser = (): AppThunk => async (dispatch) => {
    dispatch(fetchUser());
    await fetchWrapper((getUserLink()), { method: 'GET', credentials: 'include' })
        .then((json) => dispatch(fetchUserSuccess(json)))
        .catch((err) => {
            console.error(err);
            dispatch(fetchUserFailure())
        });
}