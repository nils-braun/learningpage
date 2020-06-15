import { SFC } from 'react';

import { CoursePageContent, RootState } from '../../types';
import Header from './subcomponents/Header';
import AboutSection from './subcomponents/AboutSection';
import InstructorsSection from './subcomponents/InstructorsSection';
import AnchorRow from './subcomponents/AnchorRow';
import { getContentStartLink } from '../../utils';
import { useSelector } from 'react-redux';

export interface CoursePageProps {
    page: CoursePageContent;
}

const CoursePage: SFC<CoursePageProps> = (props) => {
    const user = useSelector((state: RootState) => state.user);
    return (
        <>
            <Header
                slug={props.page.slug}
                title={props.page.title}
                subtitle={props.page.subtitle}
                hasAssignment={props.page.hasAssignment}
                allowSubmit={!user.isAnonymous}
                startLink={getContentStartLink(props.page.slug)}
            />
            <AnchorRow />
            <AboutSection
                description={props.page.description}
                learnings={props.page.learnings}
                skills={props.page.skills}
                facts={props.page.facts.map(f => ({ type: f.key, value: f.value, extra: f.extra }))}
                level={props.page.level}
            />
            <InstructorsSection
                instructors={props.page.instructors}
            />
        </>
    );
};

export default CoursePage;