import { Action } from "redux";
import { AppThunk } from "../types";
import { getContentSubmissionLink } from "../utils";

export const SUBMIT_COURSE = 'SUBMIT_COURSE';
export interface SubmitCourseAction extends Action {
    courseSlug: string;
};
const submitCourse = (slug: string): SubmitCourseAction => {
    return {
        type: SUBMIT_COURSE,
        courseSlug: slug
    };
}

export const SUBMIT_COURSE_SUCCESS = 'SUBMIT_COURSE_SUCCESS';
const submitCourseSuccess = (): Action => {
    return {
        type: SUBMIT_COURSE_SUCCESS
    };
}

export const SUBMIT_COURSE_FAILURE = 'SUBMIT_COURSE_FAILURE';
const submitCourseFailure = (): Action => {
    return {
        type: SUBMIT_COURSE_FAILURE
    };
}
export const thunkSubmitCourse = (slug: string): AppThunk => async (dispatch) => {
    dispatch(submitCourse(slug));
    await fetch(getContentSubmissionLink(slug), { method: 'POST', credentials: 'include' })
        .then(res => res.json())
        .then(() => dispatch(submitCourseSuccess()))
        .catch((err) => {
            console.error(err);
            dispatch(submitCourseFailure())
        });
}