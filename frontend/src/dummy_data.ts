import { CoursePageContent } from "./types";

export const dummyPageContent: CoursePageContent = {
    title: 'Pandas IO',
    subtitle: 'An introduction to data input and ouput with Pandas in Python',
    description: '',
    sections: [
        {
            type: 'about',
            label: 'About',
            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mauris nunc congue nisi vitae suscipit. Est placerat in egestas erat imperdiet sed. Laoreet sit amet cursus sit amet dictum sit. Facilisis mauris sit amet massa vitae tortor condimentum lacinia. In vitae turpis massa sed elementum tempus egestas sed sed. Diam sit amet nisl suscipit adipiscing bibendum. Egestas fringilla phasellus faucibus scelerisque eleifend. Amet cursus sit amet dictum. Eget est lorem ipsum dolor sit amet consectetur adipiscing elit. Sem fringilla ut morbi tincidunt augue interdum velit euismod.\n\nIn tellus integer feugiat scelerisque varius morbi enim. Massa id neque aliquam vestibulum. Vel orci porta non pulvinar. Adipiscing bibendum est ultricies integer quis. Dis parturient montes nascetur ridiculus mus mauris vitae. Felis eget nunc lobortis mattis aliquam faucibus purus in. Sit amet porttitor eget dolor morbi non arcu risus. Erat imperdiet sed euismod nisi. Proin sagittis nisl rhoncus mattis rhoncus. Consectetur a erat nam at lectus. Consectetur lorem donec massa sapien faucibus et. Mauris ultrices eros in cursus turpis massa tincidunt dui ut. At tempor commodo ullamcorper a lacus vestibulum. Quam adipiscing vitae proin sagittis nisl rhoncus mattis rhoncus urna. Augue lacus viverra vitae congue eu consequat ac felis donec. Enim neque volutpat ac tincidunt vitae semper quis lectus. Vitae congue eu consequat ac felis donec et odio pellentesque. Lectus vestibulum mattis ullamcorper velit sed ullamcorper. A arcu cursus vitae congue mauris rhoncus aenean vel elit. Aliquam sem fringilla ut morbi.\n\nLobortis scelerisque fermentum dui faucibus in ornare quam. Duis ultricies lacus sed turpis tincidunt id aliquet. Id eu nisl nunc mi ipsum faucibus vitae. Vitae suscipit tellus mauris a diam. Ultrices neque ornare aenean euismod elementum nisi quis eleifend quam. Suspendisse faucibus interdum posuere lorem ipsum. Scelerisque viverra mauris in aliquam sem fringilla. Venenatis a condimentum vitae sapien pellentesque habitant. Vestibulum morbi blandit cursus risus at ultrices. Ut tellus elementum sagittis vitae et leo duis.',
            facts: [
                {
                    type: 'level',
                    value: 'beginner',
                    prerequirements: 'You should  have beginner level experience with Python. Having skills in a common query language such as SQL is a plus.'
                },
                {
                    type: 'language',
                    value: 'english',
                    subtitles: ['english', 'german']
                }
            ],
            takeAways: {
                learnings: [
                    'You will learn how to read data from various sources',
                    'Learn about how to process data and reshape it',
                    'Learn how data can be encoded in various ways',
                    'You will see what schema evolution means and why it is important for your data',
                ],
                skills: ['File formats', 'Encoding', 'Data Wrangling', 'Data preprocessing']
            }
        },
        {
            type: 'instructors',
            label: 'Instructors',
            instructors: [
                {
                    imageUrl: '',
                    firstName: 'Larry',
                    lastName: 'Page',
                    description: 'Larry has been working for a Fortune 500 company the most of his professional time. He has been busy with being the CEO of such a company for years. Since he stepped back from this position, he loves to educate others and let people gain insights into his expert knowledge.'
                },
                {
                    imageUrl: '',
                    firstName: 'Sergey',
                    lastName: 'Brin',
                    description: 'Sergey has been working for a Fortune 500 company the most of his professional time. He has been busy with being the CTO of such a company for years. Since he stepped back from this position, he loves to educate others and let people gain insights into his expert knowledge.'
                }
            ]
        }
    ]
}