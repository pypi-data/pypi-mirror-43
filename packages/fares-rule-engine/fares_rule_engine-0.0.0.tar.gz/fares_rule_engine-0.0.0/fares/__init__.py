from typing import Dict

from fares.dimension import resolve_slot_dimensions
from fares.subscription_offering import SubscriptionOffering


def is_subscription_offering_applicable(
    subscription_offering: SubscriptionOffering, slot: Dict
):
    rule_set = subscription_offering.applicability_rules()
    context = resolve_slot_dimensions(slot)
    return rule_set.evaluate(context)
