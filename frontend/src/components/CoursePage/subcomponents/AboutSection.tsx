import { SFC } from "react";
import { markdown } from 'markdown';

import { AboutSection as IAboutSection } from "../../../types";
import TakeAwayBox from "./TakeAwayBox";
import FactItem from "./FactItem";

export interface AboutSectionProps extends IAboutSection {}

const AboutSection: SFC<AboutSectionProps> = (props) => {
    return (
        <div className="container mx-auto py-6">
            <h2 id={props.type} className="text-2xl">About this course</h2>
            <div className="grid grid-cols-3 my-4">
                <div className="mr-4 col-span-2">
                    <div className="mb-4">
                        <TakeAwayBox {...props.takeAways} />
                    </div>
                    <div dangerouslySetInnerHTML={{__html: markdown.toHTML(props.description)}}/>
                </div>
                <div>
                    <ul>
                        {props.facts.map(fact => <li key={fact.type}><FactItem {...fact} /></li>)}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default AboutSection;
