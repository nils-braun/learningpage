export interface CoursePageContent {
    title: string;
    subtitle: string;
    description: string;
    sections: CoursePageContentSection[];
}

export type CoursePageContentSection = AboutSection | InstructorsSection;

export interface CourseSection<T> {
    type: T;
    label: string;
}

export interface AboutSection extends CourseSection<'about'> {
    description: string;
    facts: CoursePageFact[];
    takeAways: CourseTakeAways;
}

export interface CourseTakeAways {
    learnings: string[];
    skills: string[];
}

export interface InstructorsSection extends CourseSection<'instructors'> {
    instructors: CourseInstructor[];
}

export type CoursePageFact = LevelFact | LanguageFact;

export type LevelValue = 'beginner' | 'intermediate' | 'advanced' | 'expert';

export interface LevelFact {
    type: 'level';
    value: LevelValue;
    prerequirements: string;
}

export interface LanguageFact {
    type: 'language';
    value: 'english' | 'german';
    subtitles: string[];
}

export interface CourseInstructor {
    imageUrl: string;
    firstName: string;
    lastName: string;
    description: string;
}