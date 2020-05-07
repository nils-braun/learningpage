import { SFC } from 'react';

import { CoursePageContent, CoursePageContentSection } from '../../types';
import { dummyPageContent } from '../../dummy_data';

import Header from './subcomponents/Header';
import AboutSection from './subcomponents/AboutSection';
import InstructorsSection from './subcomponents/InstructorsSection';
import AnchorRow from './subcomponents/AnchorRow';

export interface CoursePageProps {
    content: CoursePageContent;
}

export async function getServerSideProps() {
  return { props: { content: dummyPageContent } }
}

function renderSection(section: CoursePageContentSection) {
    switch(section.type) {
        case 'about':
            return <AboutSection key={section.type} {...section} />;
        case 'instructors':
            return <InstructorsSection key={section.type} {...section} />;
    }
}

const CoursePage: SFC<CoursePageProps> = (props) => {
    const { content } = props;
    return (
        <>
            <Header title={content.title} subtitle={content.subtitle} />
            <AnchorRow sections={content.sections} />
            {content.sections.map(renderSection)}
        </>
    )
}

export default CoursePage;