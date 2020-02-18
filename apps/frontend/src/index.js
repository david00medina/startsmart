import React from "react";
import { render } from "react-dom";

import {fas} from "@fortawesome/free-solid-svg-icons";
import {fab} from "@fortawesome/free-brands-svg-icons";
import {library} from "@fortawesome/fontawesome-svg-core";

import "@blueprintjs/core/lib/css/blueprint.css";
import "@blueprintjs/datetime/lib/css/blueprint-datetime.css";
import "@blueprintjs/select/lib/css/blueprint-select.css";
import "@blueprintjs/table/lib/css/table.css";
import "@blueprintjs/timezone/lib/css/blueprint-timezone.css";
import "@blueprintjs/icons/lib/css/blueprint-icons.css"
import "react-dropzone-uploader/dist/styles.css";

import routesConfig from "./routes.config";
import App from "./components/App";

library.add(fas, fab);

render(<App routes={routesConfig} />, document.getElementById('startsmart')
);
