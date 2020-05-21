import { SFC } from 'react';

import { CoursePageContent } from '../../types';

import Header from './subcomponents/Header';
import AboutSection from './subcomponents/AboutSection';
import InstructorsSection from './subcomponents/InstructorsSection';
import AnchorRow from './subcomponents/AnchorRow';

export interface CoursePageProps {
    content: CoursePageContent;
}

const CoursePage: SFC<CoursePageProps> = (props) => {
    const { content } = props;
    return (
        <>
            <Header
                title={content.title}
                subtitle={content.subtitle}
            />
            <AnchorRow />
            <AboutSection
                description={content.description}
                learnings={content.learnings}
                skills={content.skills}
                facts={content.facts.map(f => ({ type: f.key, value: f.value, extra: f.extra }))}
                level={content.level}
            />
            <InstructorsSection
                instructors={content.instructors}
            />
        </>
    )
}

export default CoursePage;