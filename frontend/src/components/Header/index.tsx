import { SFC } from 'react';

export interface HeaderProps {}

const Header: SFC<HeaderProps> = (props) => (
    <>
        <nav className="bg-white shadow fixed w-full z-1001">
            <div className="container mx-auto py-2 flex flex-row">
                <span className="bg-gray-300 inline-block mr-6 flex items-center justify-center" 
                    style={{height: '40px', width: '150px'}}>Logo</span>
                <input className="appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="What do you want to learn?" />
                <span className="flex-grow" />
                <button className="btn btn-blue">Log In</button>
            </div>
        </nav>
        <div style={{paddingBottom: '80px'}}/>
    </>
);

export default Header;
