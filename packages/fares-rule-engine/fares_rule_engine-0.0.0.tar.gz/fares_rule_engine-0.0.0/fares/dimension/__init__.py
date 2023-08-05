from fares.dimension.dimension import SlotDimensions


def resolve_slot_dimensions(slot):
    return {
        "slot.od_cluster_session": (
            slot[SlotDimensions.ORIGIN_CLUSTER_ID.value],
            slot[SlotDimensions.DESTINATION_CLUSTER_ID.value],
            slot[SlotDimensions.SESSION.value],
        ),
        "slot.origin_cluster_id": slot[SlotDimensions.ORIGIN_CLUSTER_ID.value],
        "slot.destination_cluster_id": slot[
            SlotDimensions.DESTINATION_CLUSTER_ID.value
        ],
        "slot.session": slot[SlotDimensions.SESSION.value],
        "slot.route_id": slot[SlotDimensions.ROUTE_ID.value],
        "slot.start_time": slot[SlotDimensions.START_TIME.value],
    }
