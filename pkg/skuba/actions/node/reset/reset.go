/*
 * Copyright (c) 2019 SUSE LLC.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

package node

import (
	"fmt"

	"github.com/SUSE/skuba/internal/pkg/skuba/deployments"
)

// Reset the target node
func Reset(resetConfiguration deployments.ResetConfiguration, target *deployments.Target) error {
	fmt.Println("[reset] resetting the node")
	return target.Apply(resetConfiguration, "kubeadm.reset")
}
