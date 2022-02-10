import {SUCCESS} from '../../timeline/state/actions'


export const acceptRequest = ({content, format, request}) => {
  return async (dispatch, getState, config) => {

    const actionsApi = config.actionsApi(request.links)


    const payload = {
      payload: {
        content,
        format: format || 'html'
      }
    }

    const response = await actionsApi.acceptRequest(payload);

    const _acceptedState = (aceptedRequest) => {

      return "SUCCESS"
    }

    dispatch({type: SUCCESS, payload: _acceptedState(response.data)})

    return response.data

  };
};

export const declineRequest = ({content, format, request}) => {
  return async (dispatch, getState, config) => {


    const actionsApi = config.actionsApi(request.links)

    const payload = {
      payload: {
        content,
        format: format || 'html'
      }
    }

    const response = await actionsApi.declineRequest(payload);

    const _declinedState = (declinedRequest) => {

      return "SUCCESS"
    }

    dispatch({type: SUCCESS, payload: _declinedState(response.data)})

    return response.data

  };
};

export const cancelRequest = ({content, format, request}) => {
  return async (dispatch, getState, config) => {


    const actionsApi = config.actionsApi(request.links)

    const payload = {
      payload: {
        content,
        format: format || 'html'
      }
    }

    const response = await actionsApi.cancelRequest(payload);

    const _canceledState = (declinedRequest) => {

      return "SUCCESS"
    }

    dispatch({type: SUCCESS, payload: _canceledState(response.data)})

    return response.data

  };
};