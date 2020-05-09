import React from "react"
import {
  ButtonSecondary,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import ThreadsStartButton from "../ThreadsStartButton"

interface IThreadsToolbarProps {
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsToolbar: React.FC<IThreadsToolbarProps> = ({ category }) => (
  <Toolbar>
    <ToolbarSeparator />
    <ToolbarItem>
      <ThreadsStartButton category={category} />
    </ToolbarItem>
  </Toolbar>
)

export default ThreadsToolbar