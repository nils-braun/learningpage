import { SFC, useEffect } from 'react';

import { CoursePageContent, RootState } from '../../types';
import Header from './subcomponents/Header';
import AboutSection from './subcomponents/AboutSection';
import InstructorsSection from './subcomponents/InstructorsSection';
import AnchorRow from './subcomponents/AnchorRow';
import { getContentStartLink } from '../../utils';
import { thunkFetchUser } from '../../actions/user';
import { connect, ConnectedProps } from 'react-redux';

export interface CoursePageOwnProps {
    page: CoursePageContent;
}

const mapState = (state: RootState) => ({
    isAnonymous: state.user.isAnonymous
});
const mapDispatch = {
    onInit: thunkFetchUser
}

const connector = connect(mapState, mapDispatch);
type CoursePagePropsFromRedux = ConnectedProps<typeof connector>;

export type CoursePageProps = CoursePagePropsFromRedux & CoursePageOwnProps;

const CoursePage: SFC<CoursePageProps> = (props) => {
    useEffect(() => {
        props.onInit();
    });

    const { page } = props;

    return (
        <>
            <Header
                slug={page.slug}
                title={page.title}
                subtitle={page.subtitle}
                hasAssignment={page.hasAssignment}
                allowSubmit={!props.isAnonymous}
                startLink={getContentStartLink(page.slug)}
            />
            <AnchorRow />
            <AboutSection
                description={page.description}
                learnings={page.learnings}
                skills={page.skills}
                facts={page.facts.map(f => ({ type: f.key, value: f.value, extra: f.extra }))}
                level={page.level}
            />
            <InstructorsSection
                instructors={page.instructors}
            />
        </>
    );
};

export default connector(CoursePage);