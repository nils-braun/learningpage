export const apiBaseUrl = 
    `http://${process.env.BACKEND_INTERNAL_HOST}${process.env.BACKEND_BASE_PATH}/api/v1`;

const externalBackendBaseUrl = 
    `http://${process.env.JUPYTERHUB_HOST}${process.env.BACKEND_BASE_PATH}`;

export const getContentSubmissionLink = (contentSlug): string =>
    `${apiBaseUrl}/content/${contentSlug}/submission`;

export const getContentStartLink = (contentSlug: string): string => 
    `${externalBackendBaseUrl}/api/v1/content/${contentSlug}/start`;