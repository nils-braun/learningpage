import { SFC } from "react";
import { markdown } from 'markdown';

import { Skill, CourseFact } from "../../../types";
import TakeAwayBox from "./TakeAwayBox";
import FactItem from "./FactItem";

export interface AboutSectionProps {
    description: string;
    learnings: string[];
    skills: Skill[];
    facts: CourseFact[];
    level: string;
}

const AboutSection: SFC<AboutSectionProps> = (props) => {
    const levelFact: CourseFact = {
        type: 'level',
        value: props.level,
        extra: {}
    };
    const facts: CourseFact[] = [levelFact, ...props.facts]
    return (
        <div className="container mx-auto py-6">
            <h2 id="about" className="text-2xl">About this course</h2>
            <div className="grid grid-cols-3 my-4">
                <div className="mr-4 col-span-2">
                    <div className="mb-4">
                        <TakeAwayBox learnings={props.learnings} skills={props.skills} />
                    </div>
                    <div dangerouslySetInnerHTML={{__html: markdown.toHTML(props.description)}}/>
                </div>
                <div>
                    <ul>
                        {facts.map(fact => <li key={fact.type}><FactItem {...fact} /></li>)}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default AboutSection;
