import { connect, ConnectedProps, MapStateToProps } from 'react-redux';

import { SFC } from "react";
import { thunkSubmitCourse } from '../../../actions/course';
import { RootState } from '../../../types';

const mapState = (state: RootState) => ({
    submissionFetching: state.course.submissionFetching,
    submissionsCount: state.course.submissionsCount
});

const mapDispatch = {
    handleSubmit: thunkSubmitCourse
};

const connector = connect(mapState, mapDispatch);

export interface HeaderOwnProps {
    slug: string;
    title: string;
    subtitle: string;
    hasAssignment: boolean;
    startLink: string;
}

type HeaderPropsFromRedux = ConnectedProps<typeof connector>;

export type HeaderProps = HeaderPropsFromRedux & HeaderOwnProps;

const Header: SFC<HeaderProps> = (props) => {
    return (
        <div className="bg-blue-500 text-white">
            <div className="container mx-auto py-6">
                <div className="grid grid-cols-1 lg:grid-cols-3">
                    <div className="lg:col-span-2 flex flex-col mb-4">
                        <h1 className="text-4xl">{props.title}</h1>
                        <div className="flex-grow">
                            <p className="text-xl">{props.subtitle}</p>
                        </div>
                    </div>
                    <div className="mb-4">
                        Offered by:
                        <img src="//via.placeholder.com/350x350" />
                    </div>
                </div>
                <div>
                    <div className="inline-block mr-8">
                        <a href={props.startLink} className="btn btn-white">Start</a>
                        <div>10.000 enrolled</div>
                    </div>
                    {props.hasAssignment && 
                        <div className="inline-block">
                            <button className="btn btn-white" 
                                onClick={() => props.handleSubmit(props.slug)}
                                disabled={props.submissionFetching}
                            >Submit</button>
                            <div>{props.submissionsCount} submissions</div>
                        </div>
                    }
                </div>
            </div>
        </div>
    );
}

export default connector(Header);