export interface ApiCoursePage {
    contentGroup: string;
    contentGroupSlug: string;
    course: string;
    courseSlug: string;
    description: string;
    facts: ApiCourseFact[];
    hasAssignment: boolean;
    instructors: ApiCourseInstructor[];
    learnings: string[];
    level: ApiCourseLevelValue;
    logoUrl: string;
    skills: ApiSkill[];
    slug: string;
    subtitle: string;
    title: string;
}

export interface ApiSkill {
    name: string;
    slug: string;
}

export type Skill = ApiSkill;

export type ApiCourseLevelValue = 'beginner' | 'intermediate' | 'advanced' | 'expert';
export type CourseLevelValue = ApiCourseLevelValue;


export interface ApiCourseInstructor {
    firstName: string;
    lastName: string;
    imageUrl: string;
    description: string;
}

export type CourseInstructor = ApiCourseInstructor;

export interface ApiCourseFact {
    key: string;
    value: string;
    extra: { [key: string]: any };
}

export type CourseFact = {
    type: string;
    value: string;
    extra: { [key: string]: any };
}

export type CoursePageContentNew = ApiCoursePage;