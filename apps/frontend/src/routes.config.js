import React from "react";

import Home from "./components/views/Home";
import ProjectCollectionView from "./components/views/ProjectView/ProjectCollectionView";
import DatasetCollectionView from "./components/views/DatasetView/DatasetCollectionView";
import Annotator from "./components/views/AnnotationView/Annotator";
import NotFound from "./components/views/NotFound";

const routesConfig = [
        {
                path: "/projects",
                component: ProjectCollectionView
        },
        {
                path: "/:projectID/datasets",
                component: DatasetCollectionView
        },
        {
                path: "/:projectID/:datasetID/annotator",
                component: Annotator
        },
        {
                path: "/",
                component: Home
        }
];

export default routesConfig;