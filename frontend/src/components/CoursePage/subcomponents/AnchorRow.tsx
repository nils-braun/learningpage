import { SFC } from "react";
import { CourseSection } from "../../../types";

export interface AnchorRowProps {
    sections: CourseSection<any>[];
}

const AnchorRow: SFC<AnchorRowProps> = (props) => {
    return (
        <div className="bg-gray-200">
            <div className="container mx-auto">
                <ul>
                    {props.sections.map(section => (
                        <li key={section.type} className="inline-block mr-8 my-4">
                            <a href={'#' + section.type}>{section.label}</a>
                        </li>)
                    )}
                </ul>
            </div>
        </div>
    );
}

export default AnchorRow;
