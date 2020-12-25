import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { useModalContext } from "../../../Context"
import { Modal, ModalDialog } from "../../../UI/Modal"
import { MutationError } from "../../../types"
import { Thread } from "../Threads.types"
import ThreadsModerationError from "./ThreadsModerationError"

interface ThreadsModerationOpenProps {
  threads: Array<Thread>
  graphqlError?: ApolloError | null
  errors?: Array<MutationError> | null
}

const ThreadsModerationOpen: React.FC<ThreadsModerationOpenProps> = ({
  threads,
  graphqlError,
  errors,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.open_threads">Open threads</Trans>}
        close={closeModal}
      >
        <ThreadsModerationError
          graphqlError={graphqlError}
          errors={errors}
          threads={threads}
          close={closeModal}
        />
      </ModalDialog>
    </Modal>
  )
}
export default ThreadsModerationOpen
