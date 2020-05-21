import { SFC } from 'react';

import { CoursePageContent } from '../../types';

import Header from './subcomponents/Header';
import AboutSection from './subcomponents/AboutSection';
import InstructorsSection from './subcomponents/InstructorsSection';
import AnchorRow from './subcomponents/AnchorRow';

export interface CoursePageProps {
    page: CoursePageContent;
}

const CoursePage: SFC<CoursePageProps> = ({ page }) => {
    return (
        <>
            <Header
                title={page.title}
                subtitle={page.subtitle}
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
    )
};

export default CoursePage;