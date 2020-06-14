import { SFC } from 'react';

import { CoursePageContent } from '../../types';

import Header from './subcomponents/Header';
import AboutSection from './subcomponents/AboutSection';
import InstructorsSection from './subcomponents/InstructorsSection';
import AnchorRow from './subcomponents/AnchorRow';
import { getContentStartLink } from '../../utils';

export interface CoursePageProps {
    page: CoursePageContent;
}

const CoursePage: SFC<CoursePageProps> = ({ page }) => {
    return (
        <>
            <Header
                slug={page.slug}
                title={page.title}
                subtitle={page.subtitle}
                hasAssignment={page.hasAssignment}
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
    )
};

export default CoursePage;