import { SFC } from "react";
import { CourseLevelValue, CourseFact } from "../../../types";

export type FactItemProps = CourseFact;

function getFactLevelTitle(level: CourseLevelValue) {
    switch (level) {
        case 'beginner':
            return 'Beginner Level';
        case 'intermediate':
            return 'Intermediate Level';
        case 'advanced':
            return 'Advanced Level';
        case 'expert':
            return 'Expert Level';
    }
}

function getIcon(type: string) {
    switch (type) {
        case 'level':
            return 'las la-signal';
        case 'language':
            return 'las la-globe';
        case 'prerequirements':
            return 'las la-star-half-alt';
        default:
            return 'las la-question';
    }
}

function getTitle(type: string, value: string) {
    switch (type) {
        case 'level':
            return getFactLevelTitle(value as CourseLevelValue)
        default:
            return value;
    }
}

const FactItem: SFC<FactItemProps> = (props) => {
    const subtitle = '';
    return (
        <div className="flex flex-row mb-8">
            <div className="mr-2">
                <i className={`text-2xl px-2 py-2 border rounded-full text-blue-500 ` + getIcon(props.type)} />
            </div>
            <div className="flex-grow">
                <p className="text-xl">{getTitle(props.type, props.value)}</p>
                <p className="text-gray-600">{subtitle}</p>
            </div>
        </div>
    )
}

export default FactItem;