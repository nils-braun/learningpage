import { SFC } from "react";
import { CoursePageFact, LevelValue } from "../../../types";

export type FactItemProps = CoursePageFact;

function getFactLevelTitle(level: LevelValue) {
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

function getFactLanguageTitle(key: string) {
    switch (key) {
        case 'english':
            return 'English';
    }
}

const FactItem: SFC<FactItemProps> = (props) => {
    let iconClass = '';
    let title = '';
    let subtitle = '';

    if (props.type == 'level') {
        iconClass = "las la-signal";
        title = getFactLevelTitle(props.value);
        subtitle = props.prerequirements;
    } else if (props.type == 'language') {
        iconClass = "las la-globe";
        title = getFactLanguageTitle(props.value);
        subtitle = 'Subtitles: ' + props.subtitles.join(', ');
    }
    return (
        <div className="flex flex-row mb-8">
            <div className="mr-2">
                <i className={`text-2xl px-2 py-2 border rounded-full text-blue-500 ` + iconClass} />
            </div>
            <div className="flex-grow">
                <p className="text-xl">{title}</p>
                <p className="text-gray-600">{subtitle}</p>
            </div>
        </div>
    )
}

export default FactItem;