from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chat_completion_response_choices import ChatCompletionResponseChoices
    from ..models.chat_completion_response_usage import ChatCompletionResponseUsage


T = TypeVar("T", bound="ChatCompletionResponse")


@_attrs_define
class ChatCompletionResponse:
    """A chat-completion response (OpenAI-compatible envelope).

    Attributes:
        id (str):
        object_ (str):  Example: chat.completion.
        created (int):
        model (str):
        choices (ChatCompletionResponseChoices): Completion choices; each carries an index, a message, and a finish
            reason.
        usage (ChatCompletionResponseUsage): Token usage accounting (prompt/completion/total).
    """

    id: str
    object_: str
    created: int
    model: str
    choices: ChatCompletionResponseChoices
    usage: ChatCompletionResponseUsage
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_ = self.object_

        created = self.created

        model = self.model

        choices = self.choices.to_dict()

        usage = self.usage.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created": created,
                "model": model,
                "choices": choices,
                "usage": usage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chat_completion_response_choices import ChatCompletionResponseChoices
        from ..models.chat_completion_response_usage import ChatCompletionResponseUsage

        d = dict(src_dict)
        id = d.pop("id")

        object_ = d.pop("object")

        created = d.pop("created")

        model = d.pop("model")

        choices = ChatCompletionResponseChoices.from_dict(d.pop("choices"))

        usage = ChatCompletionResponseUsage.from_dict(d.pop("usage"))

        chat_completion_response = cls(
            id=id,
            object_=object_,
            created=created,
            model=model,
            choices=choices,
            usage=usage,
        )

        chat_completion_response.additional_properties = d
        return chat_completion_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
