import { Reducer } from 'redux';
import { CourseState } from '../types';
import { SUBMIT_COURSE, SUBMIT_COURSE_SUCCESS, SUBMIT_COURSE_FAILURE } from '../actions/course';

const initialState: CourseState = {
    submissionFetching: false,
    submissionsCount: 0
};

const course: Reducer<CourseState> = (state = initialState, action) => {
    switch(action.type) {
        case SUBMIT_COURSE:
            return {...state, submissionFetching: true};
        case SUBMIT_COURSE_SUCCESS:
            return {...state, submissionFetching: false, submissionsCount: state.submissionsCount + 1};
        case SUBMIT_COURSE_FAILURE:
            return {...state, submissionFetching: false};
        default:
            return state;
    }
}

export default course;