import { SFC } from "react";
import { CourseTakeAways } from "../../../types";

export interface TakeAwayBoxProps extends CourseTakeAways {}

const renderLearning = (learning: string) => {
    return (
        <div key={learning} className="flex flex-row my-4">
            <i className="las la-check mr-2 text-green-600" style={{marginTop: '5px'}} /> <span className="flex-grow">{learning}</span>
        </div>
    );
}

const TakeAwayBox: SFC<TakeAwayBoxProps> = (props) => {
    return (
        <div className="border p-4">
            <div>
                <h3 className="text-gray-600 text-sm uppercase font-bold">What you will learn</h3>
                <div className="grid grid-cols-2 gap-2 mb-4">
                    <div>
                        {props.learnings
                            .filter((x, i) => i % 2 == 0 && x)
                            .map(renderLearning)}
                    </div>
                    <div>
                        {props.learnings
                            .filter((x, i) => i % 2 == 1 && x)
                            .map(renderLearning)}
                    </div>
                </div>
            </div>
            <div>
                <h3 className="text-gray-600 text-sm uppercase font-bold mb-4">Skills you will gain</h3>
                <div className="mb-2">
                    {props.skills.map(s => <span key={s} className="bg-gray-200 px-4 py-2 mr-2 rounded">{s}</span>)}
                </div>
            </div>
        </div>
    );
}

export default TakeAwayBox;