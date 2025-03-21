import React from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {

  buildSearchOptionsFromConfig,

} from "./config/config-helper";

const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "cv-transcriptions"
});
const config = {
  searchQuery: {
    facets: {
      "age.keyword": { type: "value" },
      "gender.keyword": { type: "value" },
      "accent.keyword": { type: "value" },
      duration: {
        type: "range",
        ranges: [
          { from: 0, to: 2, name: "0-2 sec" },
          { from: 2, to: 5, name: "2-5 sec" },
          { from: 5, to: 10, name: "5-10 sec" },
          { from: 10, name: "10+ sec" }
        ]
      },
      "generated_text.keyword": { type: "value" }
    },
    ...buildSearchOptionsFromConfig()
  },
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true
}

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={
                    <SearchBox
                    />
                  }
                  sideContent={
                    <div>
                      {wasSearched && <Sorting label={"Sort by"} sortOptions={[]} />}
                      <Facet key={"1"} field={"generated_text"} label={"Generated Text"} />
                      <Facet key={"2"} field={"duration"} label={"Duration"} />
                      <Facet key={"3"} field={"age"} label={"Age"} />
                      <Facet key={"4"} field={"gender"} label={"Gender"} />
                      <Facet key={"5"} field={"accent"} label={"Accent"} />
                    </div>
                  }
                  bodyContent={<Results shouldTrackClickThrough={true} />}
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>

          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
