export const apiBaseUrl = 
    `http://${process.env.BACKEND_INTERNAL_HOST}${process.env.BACKEND_BASE_PATH}/api/v1`;
export const externalApiBaseUrl =
    `http://${process.env.JUPYTERHUB_HOST}${process.env.BACKEND_BASE_PATH}/api/v1`;

const externalBackendBaseUrl = 
    `http://${process.env.JUPYTERHUB_HOST}${process.env.BACKEND_BASE_PATH}`;

export const getContentSubmissionLink = (contentSlug): string =>
    `${apiBaseUrl}/content/${contentSlug}/submission`;

export const getUserLink = (): string => `${externalApiBaseUrl}/user`;

export const getContentStartLink = (contentSlug: string): string => 
    `${externalBackendBaseUrl}/api/v1/content/${contentSlug}/start`;

export const wait = <T>(value: T, timeMs: number, err: boolean = false): Promise<T> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (err) reject(value)
            else resolve(value)
        }, timeMs);
    })
}

export const fetchWrapper = async (input: RequestInfo, init?: RequestInit): Promise<any> => {
    return fetch(input, init)
        // .then(res => wait(res, 2000))  // for debugging purposes
        .then(res => {
            if (!res.ok) {
                return Promise.reject(new Error('Reponse not okay.'));
            }
            return res;
        })
        .then(res => res.json());
}