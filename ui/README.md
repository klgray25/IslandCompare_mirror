# IslandCompare front-end

Currently the front-end will expect the Galaxy instance to be located at the same domain with a 'galaxy.' subdomain.
ie. if the frontend is hosted at `http://islandcompare.mysite.com`, Galaxy is expected to be accessible via `http://galaxy.mysite.com`.

The workflow in the backend is targeted by name, currently configured to 'IslandCompare unpacked'. This workflow must be shared public in the workflow settings of Galaxy.

**See [src/app.config.js](src/app.config.js) for configuration parameters.**

## Notes
- Datasets are stored in a history tagged 'user_data'
- Each job gets its own history tagged with the workflow id
- Update vue.config.js/publicPath and src/app.config.js/base_path if the webpage path root is not '/'
- Static content is stored in markdown files in static/. See https://github.com/markdown-it/markdown-it for syntax extensions.

## Files
- src/components - items reusable for other galaxy projects
- src/IslandCompare - components specific to brinkman lab
- src/galaxy - Galaxy client subrepo containing all galaxy specific code. See https://github.com/brinkmanlab/galaxy-client/
- src/auth.js - all code related to authenticating with the backend
- src/store.js - Vuex init code 
- src/main.js - main entry point of app
- src/app.js - all code specifically for loading and invoking IslandCompare state
- src/tour.js - Analysis tour steps
- src/brinkman_services.js - list of available brinkman services
- gulpfile.js - responsible for all preprocessing before webpack is invoked


## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your tests
```
npm run test
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
