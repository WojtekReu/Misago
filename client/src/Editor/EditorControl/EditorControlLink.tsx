import React from "react"
import Icon from "../../UI/Icon"
import { IEditorControlProps } from "./EditorControl.types"
import EditorButton from "../EditorButton"
import EditorControlLinkModal from "./EditorControlLinkModal"

const EditorControlLink: React.FC<IEditorControlProps> = ({
  title,
  icon,
  context,
}) => {
  const { disabled } = context
  const [isOpen, setOpen] = React.useState(false)

  return (
    <>
      <EditorButton
        className="btn-editor-link"
        disabled={disabled}
        title={title}
        icon
        onClick={() => setOpen(true)}
      >
        <Icon icon={icon} fixedWidth />
      </EditorButton>
      <EditorControlLinkModal
        context={context}
        isOpen={isOpen}
        close={() => setOpen(false)}
      />
    </>
  )
}

export default EditorControlLink
