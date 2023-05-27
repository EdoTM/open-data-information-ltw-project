FROM node:18-alpine
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN ["npm", "install"]
COPY . .
EXPOSE 5173
ARG BUILD
RUN if [ "$BUILD" = "true" ] ; then npm run build ; fi