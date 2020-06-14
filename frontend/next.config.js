module.exports = {
    env: {
        BASE_PATH: process.env.BASE_PATH,
        BACKEND_BASE_PATH: process.env.BACKEND_BASE_PATH,
        BACKEND_INTERNAL_HOST: process.env.BACKEND_INTERNAL_HOST,
        JUPYTERHUB_HOST: process.env.JUPYTERHUB_HOST,
    },
    experimental: {
        basePath: process.env.BASE_PATH || '',
    },
}