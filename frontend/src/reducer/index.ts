import { combineReducers } from 'redux'

import user from './user';
import course from './course';
import { RootState } from '../types';

const rootReducer = combineReducers<RootState>({
    user,
    course
});

export default rootReducer;
