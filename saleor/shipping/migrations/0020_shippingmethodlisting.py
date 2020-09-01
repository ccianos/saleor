# Generated by Django 3.1 on 2020-08-24 10:09

import django.db.models.deletion
from django.db import migrations, models


def create_shipping_method_channel_listing(apps, schema_editor):
    ShippingMethod = apps.get_model("shipping", "ShippingMethod")
    ShippingMethodChannelListing = apps.get_model(
        "shipping", "ShippingMethodChannelListing"
    )
    Channel = apps.get_model("channel", "Channel")

    channels_dict = {}

    for shipping_method in ShippingMethod.objects.iterator():
        currency = shipping_method.currency
        channel = channels_dict.get(currency)
        if not channel:
            channel, _ = Channel.objects.get_or_create(
                currency_code=currency,
                defaults={
                    "name": f"Channel {currency}",
                    "slug": f"channel-{currency.lower()}",
                },
            )
            channels_dict[currency] = channel
        if shipping_method.type == "price":
            max_value = shipping_method.maximum_order_price_amount
            min_value = shipping_method.minimum_order_price_amount
        else:
            max_value, min_value = None, None
        ShippingMethodChannelListing.objects.create(
            channel=channel,
            shipping_method=shipping_method,
            maximum_order_price_amount=max_value,
            minimum_order_price_amount=min_value,
            price_amount=shipping_method.price_amount,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("channel", "0001_initial"),
        ("shipping", "0019_remove_shippingmethod_meta"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShippingMethodChannelListing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "minimum_order_price_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        null=True,
                    ),
                ),
                ("currency", models.CharField(default="USD", max_length=3)),
                (
                    "maximum_order_price_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "price_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipping_method_listing",
                        to="channel.channel",
                    ),
                ),
                (
                    "shipping_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channel_listing",
                        to="shipping.shippingmethod",
                    ),
                ),
            ],
            options={
                "ordering": ("pk",),
                "unique_together": {("shipping_method", "channel")},
            },
        ),
        migrations.RunPython(create_shipping_method_channel_listing),
        migrations.RemoveField(
            model_name="shippingmethod", name="maximum_order_price_amount",
        ),
        migrations.RemoveField(
            model_name="shippingmethod", name="minimum_order_price_amount",
        ),
        migrations.RemoveField(model_name="shippingmethod", name="price_amount",),
    ]
