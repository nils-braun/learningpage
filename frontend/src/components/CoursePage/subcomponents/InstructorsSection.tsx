import { SFC } from "react";
import { InstructorsSection as IInstructorsSection } from '../../../types';
import { markdown } from 'markdown';

export interface InstructorsSectionProps extends IInstructorsSection {}

const InstructorsSection: SFC<InstructorsSectionProps> = (props) => {
    return (
        <div key={props.type}>
            <div className="container mx-auto py-6">
                <h2 id={props.type} className="text-2xl">Course Instructors</h2>
                <div className="my-4">
                    {props.instructors.map(instructor => (
                        <div key={instructor.firstName + instructor.lastName} className="flex flex-row mb-4">
                            <img
                                src="//via.placeholder.com/200x200"
                                alt={`Image of instructor ${instructor.firstName} ${instructor.lastName}`}
                                className="mr-4"
                            />
                            <div>
                                <h4 className="text-xl">{instructor.firstName} {instructor.lastName}</h4>
                                <div dangerouslySetInnerHTML={{__html: markdown.toHTML(instructor.description)}} />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default InstructorsSection;