from django import template
import calendar

register = template.Library()


@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]

@register.filter
def weekday_name(weekday_number):
    return calendar.day_name[weekday_number-1]
