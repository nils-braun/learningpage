import { SFC } from "react";

export interface HeaderProps {
    title: string;
    subtitle: string;
}

const Header: SFC<HeaderProps> = (props) => {
    return (
        <div className="bg-blue-500 text-white">
            <div className="container mx-auto py-6">
                <div className="grid grid-cols-1 lg:grid-cols-3">
                    <div className="lg:col-span-2 flex flex-col mb-4">
                        <h1 className="text-4xl">{props.title}</h1>
                        <div className="flex-grow">
                            <p className="text-xl">{props.subtitle}</p>
                        </div>
                    </div>
                    <div className="mb-4">
                        Offered by:
                        <img src="//via.placeholder.com/350x350" />
                    </div>
                </div>
                <div>
                    <div className="inline-block mr-8">
                        <button className="btn btn-white">Start</button>
                        <div>10.000 enrolled</div>
                    </div>
                    <div className="inline-block">
                        <button className="btn btn-white">Submit</button>
                        <div>x submissions</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Header;