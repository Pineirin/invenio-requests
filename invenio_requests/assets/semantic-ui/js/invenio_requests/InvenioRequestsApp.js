import { InvenioRequestsTimelineAPI, RequestLinkExtractor, ActionsApi} from "./api/api";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { configureStore } from "./store";
import { OverridableContext } from "react-overridable";
import RequestDetails from "./RequestDetails";
import { RequestAction } from "./requestAction";
import { Provider } from "react-redux";

export class InvenioRequestsApp extends Component {
  constructor(props) {
    super(props);
    const { requestsApi, actionsApi, request } = this.props;
    const defaultRequestsApi = new InvenioRequestsTimelineAPI(
      new RequestLinkExtractor(request.links)
    );
    const defaultActionsApi = (actionLinks) => new ActionsApi(actionLinks)

    const appConfig = {
      requestsApi: requestsApi || defaultRequestsApi,
      actionsApi: actionsApi || defaultActionsApi,
      request,
      refreshIntervalMs: 5000,
    };
    this.store = configureStore(appConfig);
  }

  render() {
    const { overriddenCmps, request } = this.props;
    return (
      <OverridableContext.Provider value={overriddenCmps}>
        <Provider store={this.store}>
          <RequestAction />
          <RequestDetails />
        </Provider>
      </OverridableContext.Provider>
    );
  }
}

InvenioRequestsApp.propTypes = {
  requestsApi: PropTypes.object,
  actionsApi: PropTypes.object,
  overriddenCmps: PropTypes.object,
  request: PropTypes.object.isRequired,
};

InvenioRequestsApp.defaultProps = {
  overriddenCmps: {},
  requestsApi: null,
  actionsApi: null,
};
