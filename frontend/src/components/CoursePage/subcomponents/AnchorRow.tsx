import { SFC } from "react";

export interface AnchorRowProps {
}

const AnchorRow: SFC<AnchorRowProps> = () => {
    return (
        <div className="bg-gray-200">
            <div className="container mx-auto">
                <ul>
                    <li className="inline-block mr-8 my-4"><a href='#about'>About</a></li>
                    <li className="inline-block mr-8 my-4"><a href='#instructors'>Instructors</a></li>
                </ul>
            </div>
        </div>
    );
}

export default AnchorRow;
