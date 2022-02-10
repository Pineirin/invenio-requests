import RequestActionComponent from "./RequestAction";
import { connect } from "react-redux";
import { acceptRequest, declineRequest, cancelRequest } from "./state/actions";

const mapStateToProps = (state) => ({
  request: state.request,
});

const mapDispatchToProps = (dispatch) => ({
  acceptRequest: async (payload) => dispatch(acceptRequest(payload)),
  declineRequest: async (payload) => dispatch(declineRequest(payload)),
  cancelRequest: async (payload) => dispatch(cancelRequest(payload)),
});

export const RequestAction = connect(
  mapStateToProps,
  mapDispatchToProps
)(RequestActionComponent);
